# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



from cegalprizm.pythontool.petrelobject import PetrelObject

import typing
import math
import pandas as pd

from cegalprizm.pythontool import primitives
from cegalprizm.pythontool import _utils
from cegalprizm.pythontool import exceptions
from cegalprizm.pythontool import borehole
from cegalprizm.pythontool._system import _system

if typing.TYPE_CHECKING:
    from cegalprizm.pythontool.grpc.borehole_grpc import DiscreteGlobalWellLogGrpc, GlobalWellLogGrpc, WellLogGrpc, DiscreteWellLogGrpc
    from cegalprizm.pythontool.borehole import Well

class LogSample(object):
    """An object representing a log sample, holding its position and value"""

    def __init__(self, md: float, x, y, z, twt:float, tvd:float, value:float, is_discrete):
        self._is_discrete = is_discrete
        self._missing_value = (
            _system().Int32.MaxValue if is_discrete else _system().Double.NaN
        )
        self._md = md
        self._twt = twt
        self._tvd = tvd
        self._position: primitives.Point = primitives.Point(x, y, z)
        if self._is_missing_value(value):
            self._value = None
        else:
            self._value = value

    def __str__(self) -> str:
        """A readable representation of the sample"""
        return "LogSample(md={:.2f}, position={}, TWT={:.2f}, TVD={:.2f}, value={})".format(
            self._md, str(self._position), self._twt, self._tvd, self._value_text()
        )

    def __repr__(self) -> str:
        return str(self)

    def _is_missing_value(self, v):
        if self._is_discrete:
            return v is None or v == _system().Int32.MaxValue
        else:
            return v is None or math.isnan(v)

    def _value_text(self):
        if self.value is None:
            return str(None)
        else:
            return (
                "{}".format(self.value)
                if self._is_discrete
                else "{:.2f}".format(self._value)
            )

    @property
    def position(self) -> primitives.Point:
        """The position of the sample in world-coordinates

        Returns:
            cegalprizm.pythontool.Point: the world coordinates of the sample

        """
        return self._position

    @property
    def md(self) -> float:
        """Returns the measured depth of the sample"""
        return self._md

    @property
    def twt(self) -> float:
        """The two-way-time value of the sample

        Use this value instead of the ``z`` property of the
        ``position`` property when you want to work with logs and
        seismic objects in the time domain as opposed to objects in
        the depth domain.

        Returns:
            The TWT of the sample in the time domain.

        """
        return self._twt


    @property
    def tvd(self) -> float:
        """Returns the true vertical depth of the sample"""
        return self._tvd

    @property
    def value(self) -> typing.Optional[float]:
        """Gets and sets the value of the log sample

        N.b no conversion of units is made from Petrel. For discrete
        logs, the values are integers you can then map the integer
        values to strings using the log's ``discrete_codes`` property.

        Note that setting a sample's value in this way can be very
        slow, especially if you are setting lots of them one after the
        other down a log.  In this case, consider using
        :func:`cegalprizm.pythontool.WellLog.set_values` or calling
        :func:`cegalprizm.pythontool.LogSamples.clone` object to create a
        'disconnected' `LogSamples`.  When disconnected, setting the
        values individually is speedy. You can then use the `samples`
        property to assign the `LogSamples` object to the well.

        Raises:
            PythonToolException: if the log is read-only
            ValueError: if the log is discrete and the value is not an integer

        """
        return self._value

    @value.setter
    def value(self, v):
        if v is not None and self._is_discrete and type(v) is not int:
            raise ValueError(
                "can only set integer values or None for a discrete well log"
            )

        v2 = v
        if v2 is None:
            v2 = self._missing_value
        self._value = v

class LogSamples(object):
    """An object containing all the samples for a particular well log

    A ``LogSamples`` object contains multiple :class:`cegalprizm.pythontool.LogSample` objects.
    These can be iterated over, accessed by index, or queried by measured-depth.

    **Example**:

    .. code-block:: python

      # print all the samples' measured depths and values
      for sample in mylog.samples:
          print(sample.md, " --> ", sample.value)

      # print the 100th sample
      print(mylog.samples[99])

      # print the sample with measured depth 1000
      # n.b if there is no sample at that depth, None is returned
      print(mylog.samples.at(1000))

    """

    def __init__(self, samples):
        self._samples = samples

    def at(self, md: float) -> typing.Optional[LogSample]:
        """The log sample at the specified measured depth

        Args:
            md: the measured depth

        Returns:
            The log sample, or `None` if no sample is at that depth.

        """
        for s in self:
            if _utils.about_equal(s.md, md):
                return s
        return None

    def __getitem__(self, idx: int) -> LogSample:
        return self._samples[idx] # type: ignore

    def __iter__(self) -> typing.Iterator[LogSample]:
        idx = 0
        while idx < len(self._samples):
            yield self._samples[idx]
            idx += 1

    def __len__(self) -> int:
        return len(self._samples)

    def __str__(self) -> str:
        return "LogSamples(welllog=%s, count=%s)" % ("disconnected", len(self._samples))

class WellLog(PetrelObject):
    """A class holding information about a continuous well log"""

    def __init__(self, petrel_object_link: "WellLogGrpc"):
        super(WellLog, self).__init__(petrel_object_link)
        self._welllog_object_link = petrel_object_link
        self._samples: typing.Optional["LogSamples"] = None

    def __str__(self) -> str:
        """A readable representation of the Well Log"""
        return 'WellLog(petrel_name="{0}")'.format(self.petrel_name)

    @property
    def well(self) -> typing.Optional["Well"]:
        """The well to which this log is measured down

        Returns:
            cegalprizm.pythontool.Well: the well for this log"""
        py_well = self._welllog_object_link.GetParentPythonBoreholeObject()
        if py_well:
            return borehole.Well(py_well)
        else:
            return None

    @property
    def unit_symbol(self) -> typing.Optional[str]:
        """The symbol for the unit which the values are measured in

        Returns:

            string: The symbol for the unit, or None if no unit is used
        """
        return _utils.str_or_none(self._welllog_object_link.GetDisplayUnitSymbol())

    @property
    def global_well_log(self) -> "GlobalWellLog":
        """The global well log this log is an instance of

        Returns:
            cegalprizm.pythontool.GlobalWellLog: the global well log for this log"""
        return GlobalWellLog(self._welllog_object_link.GetGlobalWellLog())

    def clone(self, name_of_clone: str, copy_values: bool = False) -> "WellLog":
        """ Creates a clone of the Petrel object.

        The clone is placed in the same collection as the source object.
        A clone cannot be created with the same name as an existing Petrel object in the same collection.

        This is a Python Tool Pro function and is not available when running scripts in the editor integrated in Python Tool or in a workflow.
        
        Parameters:
            path_of_clone: Petrel name of the clone
            copy_values: Set to True if values shall be copied into the clone. Defaults to False.

        Returns:
            WellLog: The clone
            
        Raises:
            Exception: If there already exists a Petrel object with the same name
            ValueError: If name_of_clone is empty or contains slashes
        """
        return typing.cast("WellLog", self._clone(name_of_clone, copy_values = copy_values))

    def _refresh_samples(self):
        cs_samples = self._petrel_object_link.Samples()
        if cs_samples is None:
            cs_samples = []
        disconnected_samples = [
            LogSample(
                s.Md, s.X, s.Y, s.ZMd, s.ZTwt, s.ZTvd, s.Value, False
            )
            for s in cs_samples
        ]

        self._samples = LogSamples(disconnected_samples)

    @property
    def samples(self) -> LogSamples:
        """Gets or sets the log samples in the form of a :class:`cegalprizm.pythontool.LogSamples` object.
            The new LogSamples object is disconnected from any Petrel object.

        Note: 
            It is recommened to use the method .set_values() instead when working with WellLogs.

        Raises:
            PythonToolException: if the log is readonly
            ValueError: if the supplied value is not a `cegalprizm.pythontool.LogSamples` object
        """
        if self._samples is None:
            self._refresh_samples()
        return self._samples

    @samples.setter
    def samples(self, logsamples: LogSamples) -> None:
        if self.readonly:
            raise exceptions.PythonToolException("Log is readonly")
        if not isinstance(logsamples, LogSamples):
            raise ValueError("Value supplied is not a LogSamples object")
        mds = []
        values = []
        for s in logsamples:
            mds.append(s.md)
            values.append(s.value)
        self.set_values(mds, values)

    def set_values(self, mds: typing.List[float], values: typing.List[typing.Optional[float]]) -> None:
        """Replaces all the log samples with the supplied measured depths and values

        Args:
            mds: a list of measured depths, one per sample
            values: a list of values, one per sample

        Raises:
            PythonToolException: if the log is readonly
            ValueError: if the measured depths and values are of difference lengths
            """
        if self.readonly:
            raise exceptions.PythonToolException("Log is readonly")
        if len(mds) != len(values):
            raise ValueError("mds and values must be the same length")

        vals = [v if v is not None else self.missing_value for v in values]

        self._welllog_object_link.SetSamples(_utils.floatarray(mds), _utils.floatarray(vals))
        self._refresh_samples()

    def as_dataframe(self) -> pd.DataFrame:
        """The values of the log as a Pandas DataFrame

        This method is only available in CPython."""
        samples_generator = (
            (s.position.x, s.position.y, s.position.z, s.md, s.twt, s.tvd, s.value)
            for s in self.samples
        )
        df = pd.DataFrame(
            samples_generator, columns=["X", "Y", "Z", "MD", "TWT", "TVD", "Value"]
        )
        return df

    @property
    def missing_value(self) -> float:
        """The value interpreted by Petrel as a 'missing' one"""
        return float("nan")

class GlobalWellLog(PetrelObject):
    def __init__(self, python_petrel_global_well_log: "GlobalWellLogGrpc"):
        super(GlobalWellLog, self).__init__(python_petrel_global_well_log)
        self._logs: typing.Optional[Logs] = None
        self._globalwelllog_object_link = python_petrel_global_well_log

    def log(self, well_name: str) -> WellLog:
        """The well log for the well specified

        Args: 
            well_name: The Petrel name of the well
    
        Returns:
            A cegalprizm.pythontool.WellLog object
        """

        var = self._globalwelllog_object_link.GetWellLogByBoreholeName(well_name)
        if (var == None):
            raise exceptions.PythonToolException("Cannot find log for the given well_name: " + well_name)
        return WellLog(var)

    @property
    def logs(self) -> "Logs":
        """An iterable collection of well logs of the Global Well Log.
        
        Returns:
            cegalprizm.pythontool.Logs: the logs of the Global Well Log.
        """      
        if self._logs is None:
            self._logs = Logs(self)
        return self._logs

    def clone(self, name_of_clone: str, copy_values : bool = False) -> "GlobalWellLog":
        """ Creates a clone of the Petrel object.

        The clone is placed in the same collection as the source object.
        A clone cannot be created with the same name as an existing Petrel object in the same collection.

        This is a Python Tool Pro function and is not available when running scripts in the editor integrated in Python Tool or in a workflow.
        
        Parameters:
            path_of_clone: Petrel name of the clone
            copy_values: Set to True if values shall be copied into the clone. Defaults to False.

        Returns:
            GlobalWellLog: The clone
            
        Raises:
            Exception: If there already exists a Petrel object with the same name
            ValueError: If name_of_clone is empty or contains slashes
        """
        return typing.cast("GlobalWellLog", self._clone(name_of_clone, copy_values = copy_values))

    def __str__(self) -> str:
        """A readable representation of the Global Well Log"""
        return 'GlobalWellLog(petrel_name="{0}")'.format(self.petrel_name)

    @property
    def unit_symbol(self) -> typing.Optional[str]:
        """The symbol for the unit which the values are measured in

        Returns:

            string: The symbol for the unit, or None if no unit is used
        """
        return _utils.str_or_none(self._globalwelllog_object_link.GetDisplayUnitSymbol())

class DiscreteGlobalWellLog(PetrelObject):
    def __init__(self, python_petrel_global_well_log: "DiscreteGlobalWellLogGrpc"):
        super(DiscreteGlobalWellLog, self).__init__(python_petrel_global_well_log)
        self._logs: typing.Optional[Logs] = None
        self._discreteglobalwelllog_object_link = python_petrel_global_well_log

    def log(self, well_name: str) -> "DiscreteWellLog":
        """The discrete well log for the well specified

        Args: 
            well_name: The Petrel name of the well
    
        Returns:
            cegalprizm.pythontool.DiscreteWellLog
        """
        var = self._discreteglobalwelllog_object_link.GetWellLogByBoreholeName(well_name)
        if (var == None):
            raise exceptions.PythonToolException("Cannot find \""+ self.petrel_name + "\" log for the given well_name: \"" + well_name + "\"")
        return DiscreteWellLog(var)

    @property
    def logs(self) -> "Logs":
        """An iterable collection of discrete well logs of the Global Well Log.
        
        Returns:
            cegalprizm.pythontool.Logs: the discrete logs of the Global Well Log.
        """ 
        if self._logs is None:
            self._logs = Logs(self)
        return self._logs

    def clone(self, name_of_clone: str, copy_values: bool = False) -> "DiscreteGlobalWellLog":
        """ Creates a clone of the Petrel object.

        The clone is placed in the same collection as the source object.
        A clone cannot be created with the same name as an existing Petrel object in the same collection.

        This is a Python Tool Pro function and is not available when running scripts in the editor integrated in Python Tool or in a workflow.
        
        Parameters:
            path_of_clone (str): Petrel name of the clone
            copy_values (bool): Set to True if values shall be copied into the clone. Defaults to False.

        Returns:
            DiscreteGlobalWellLog: The clone
            
        Raises:
            Exception: If there already exists a Petrel object with the same name
            ValueError: If name_of_clone is empty or contains slashes
        """
        return typing.cast("DiscreteGlobalWellLog", self._clone(name_of_clone, copy_values = copy_values))


    def __str__(self) -> str:
        """A readable representation of the Discrete Global Well Log"""
        return 'DiscreteGlobalWellLog(petrel_name="{0}")'.format(self.petrel_name)


class DiscreteWellLog(PetrelObject):
    """A class holding information about a discrete well log."""

    def __init__(self, python_petrel_welllog: "DiscreteWellLogGrpc"):
        super(DiscreteWellLog, self).__init__(python_petrel_welllog)
        self._samples = None
        self._discrete_codes: typing.Optional[typing.Dict[int, str]] = None
        self._discretewelllog_object_link = python_petrel_welllog

    def __str__(self) -> str:
        """A readable representation of the Well Log"""
        return 'DiscreteWellLog(petrel_name="{0}")'.format(self.petrel_name)

    @property
    def well(self) -> "Well":
        """The well to which this log is measured down

        Returns:
            cegalprizm.pythontool.Well: the well for this log"""
        return borehole.Well(self._discretewelllog_object_link.GetParentPythonBoreholeObject())

    @property
    def unit_symbol(self) -> None:
        """The symbol for the unit which the values are measured in

        Returns:

            string: The symbol for the unit, or None if no unit is used
        """    
        return None

    def clone(self, name_of_clone: str, copy_values: bool = False) -> "DiscreteWellLog":
        """ Creates a clone of the Petrel object.

        The clone is placed in the same collection as the source object.
        A clone cannot be created with the same name as an existing Petrel object in the same collection.

        This is a Python Tool Pro function and is not available when running scripts in the editor integrated in Python Tool or in a workflow.
        
        Parameters:
            path_of_clone (str): Petrel name of the clone
            copy_values (bool): Set to True if values shall be copied into the clone. Defaults to False.

        Returns:
            DiscreteWellLog: The clone
            
        Raises:
            Exception: If there already exists a Petrel object with the same name
            ValueError: If name_of_clone is empty or contains slashes
        """
        return typing.cast("DiscreteWellLog", self._clone(name_of_clone, copy_values = copy_values))

    def _refresh_samples(self):
        is_discrete = isinstance(self._petrel_object_link, DiscreteWellLog)
        cs_samples = self._petrel_object_link.Samples()
        if cs_samples is None:
            cs_samples = []
        disconnected_samples = [
            LogSample(
                s.Md, s.X, s.Y, s.ZMd, s.ZTwt, s.ZTvd, s.Value, True
            )
            for s in cs_samples
        ]

        self._samples = LogSamples(disconnected_samples)

    @property
    def samples(self) -> LogSamples:
        """Gets or sets the log samples in the form of a :class:`cegalprizm.pythontool.LogSamples` object

        Raises:
            PythonToolException: if the log is readonly
            ValueError: if the supplied value is not a `cegalprizm.pythontool.LogSamples` object
        """
        if self._samples is None:
            self._refresh_samples()
        return self._samples

    @samples.setter
    def samples(self, logsamples: LogSamples):
        if self.readonly:
            raise exceptions.PythonToolException("Log is readonly")
        if not isinstance(logsamples, LogSamples):
            raise ValueError("Value supplied is not a LogSamples object")
        mds = []
        values = []
        for s in logsamples:
            mds.append(s.md)
            values.append(s.value)
        self.set_values(mds, values)

    def set_values(self, mds: typing.List[float], values: typing.List[typing.Optional[float]]):
        """Replaces all the log samples with the supplied measured depths and values

        Args:
            mds: a list of measured depths, one per sample
            values: a list of values, one per sample

        Raises:
            PythonToolException: if the log is readonly
            ValueError: if the measured depths and values are of difference lengths
        """
        if len(mds) != len(values):
            raise ValueError("mds and values must be the same length")
        if self.readonly:
            raise exceptions.PythonToolException("Log is readonly")

        vals = [v if not ((v is None) or (math.isnan(v))) else self.missing_value for v in values]

        self._discretewelllog_object_link.SetSamples(_utils.floatarray(mds), _utils.intarray(vals))
        self._refresh_samples()

    @property
    def discrete_codes(self) -> typing.Dict[int, str]:
        """A dictionary of discrete codes and values

        Changes to this dictionary will not be persisted or affect any Petrel objects.

        **Example:**

        .. code-block:: Python

            mylog = petrellink.welllog['facies']
            print(mylog.discrete_codes[1])
            # outputs 'Fine sand'
        """
        if self._discrete_codes is None:
            self._discrete_codes = self.__make_discrete_codes_dict()
        return self._discrete_codes

    @property
    def global_well_log(self) -> DiscreteGlobalWellLog:
        """The global well log this log is an instance of

        Returns:
            cegalprizm.pythontool.DiscreteGlobalWellLog: the global well log for this log"""
        return DiscreteGlobalWellLog(self._discretewelllog_object_link.GetGlobalWellLog())

    def __make_discrete_codes_dict(self) -> typing.Dict[int, str]:
        codes = {}
        for tup in self._discretewelllog_object_link.GetAllDictionaryCodes():
            k = tup.Item1
            v = tup.Item2
            codes[k] = v
        self._discrete_codes = codes
        return codes

    def __value_text(self, sample):
        value_text = "" if sample.value is None else self.discrete_codes[sample.value]
        return value_text

    def as_dataframe(self) -> pd.DataFrame:
        """The values of the log as a Pandas DataFrame

        This method is only available in CPython."""
        import pandas as pd

        samples_unpacked = (
            (
                s.position.x,
                s.position.y,
                s.position.z,
                s.md,
                s.twt,
                s.tvd,
                s.value,
                self.__value_text(s),
            )
            for s in self.samples
        )
        df = pd.DataFrame(
            samples_unpacked, columns=["X", "Y", "Z", "MD", "TWT", "TVD", "Value", "ValueText"]
        )
        return df

    @property
    def missing_value(self) -> int:
        """The value interpreted by Petrel as a 'missing' one"""
        return _system().Int32.MaxValue # type: ignore


class Logs(object):
    """An iterable collection of :class:`cegalprizm.pythontool.WellLog` and :class:`cegalprizm.pythontool.DiscreteWellLog`
    objects for the logs belonging to this well."""

    def __init__(self, parent):
        # import here to break cyclical dependecy welllog -> borehole -> welllog
        from cegalprizm.pythontool import WellLog, DiscreteWellLog, Well

        if isinstance(parent, Well):
            self._parent_is_well = True
            borehole = parent
            self._logs = [
                WellLog(log)
                for log in borehole._borehole_object_link.GetAllContinuousLogs()
            ]
            self._logs.extend(
                [
                    DiscreteWellLog(log)
                    for log in borehole._borehole_object_link.GetAllDictionaryLogs()
                ]
            )
        elif isinstance(parent, GlobalWellLog):
            self._parent_is_well = False
            gwl = parent
            self._logs = [
                WellLog(cs_welllog)
                for cs_welllog in gwl._globalwelllog_object_link.GetAllWellLogs()
            ]
        elif isinstance(parent, DiscreteGlobalWellLog):
            self._parent_is_well = False
            gwl = parent
            self._logs = [
                DiscreteWellLog(cs_welllog)
                for cs_welllog in gwl._discreteglobalwelllog_object_link.GetAllWellLogs()
            ]
        else:
            raise TypeError(
                "Parent must be Well, GlobalWellLog or DiscreteGlobalWellLog"
            )

    def __getitem__(self, key: str) -> typing.Union[WellLog, DiscreteWellLog]:
        def key_extractor_log_name(log):
            return log.petrel_name

        def key_extractor_well_name(log):
            return log.well.petrel_name

        # if the Logs owner is a well, then the logs are of different name and we'd be searching by name,
        # if the owner is a Global Well Log then the logs are of the same name and we'd be searching by borehole
        key_func = (
            key_extractor_log_name
            if self._parent_is_well
            else key_extractor_well_name
        )
        matching = [l for l in self._logs if key_func(l) == key]
        if len(matching) == 1:
            return matching[0] # type: ignore
        else:
            raise KeyError("Cannot find unique log name " + key)

    def __iter__(self) -> typing.Iterator[typing.Union[WellLog, DiscreteWellLog]]:
        return iter(self._logs)

    def __len__(self) -> int:
        return len(self._logs)
