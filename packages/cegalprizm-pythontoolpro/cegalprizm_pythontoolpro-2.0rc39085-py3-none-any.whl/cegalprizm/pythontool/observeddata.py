# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



import pandas as pd
import typing
import datetime
from cegalprizm.pythontool.petrelobject import PetrelObject
from cegalprizm.pythontool import _utils
from cegalprizm.pythontool.exceptions import PythonToolException
from cegalprizm.pythontool import borehole


if typing.TYPE_CHECKING:
    from cegalprizm.pythontool.grpc.observeddata_grpc import ObservedDataGrpc, ObservedDataSetGrpc
    from cegalprizm.pythontool.borehole import Well

class ObservedData(PetrelObject):
    """A class holding information about observed data"""

    def __init__(self, petrel_object_link: "ObservedDataGrpc") -> None:
        super(ObservedData, self).__init__(petrel_object_link)
        self._observed_data_object_link = petrel_object_link

    def __str__(self) -> str:
        """A readable representation of the observed data"""
        return 'ObservedData(petrel_name="{0}")'.format(self.petrel_name)

    @property
    def observed_data_set(self) -> "ObservedDataSet":
        """Returns the parent observed data set"""
        return ObservedDataSet(self._observed_data_object_link.GetParentObservedDataSet())

    @property
    def unit_symbol(self) -> typing.Optional[str]:
        """Returns the symbol of the object unit, None if template of object is unitless."""
        return self._unit_symbol()

    @property
    def values(self) -> typing.List[float]:
        """Returns the values of the observed data"""
        return [item for item in self._observed_data_object_link.GetValues()]

    def set_values(self, values: typing.List[float]) -> None:
        """Replaces all the values with the supplied values

        Args:
            values: a list of values, one per date in the observed data set
        """
        self._observed_data_object_link.SetValues(values)

    def as_dataframe(self) -> pd.DataFrame:
        """The values of the observed data as a Pandas dataframe."""        
        import pandas as pd
        df =  pd.DataFrame()
        df['Date'] = [date for date in self.observed_data_set.dates]
        df[self.petrel_name] = self.values
        return df

    def _unit_symbol(self) -> typing.Optional[str]:
        return _utils.str_or_none(self._observed_data_object_link.GetDisplayUnitSymbol())

class WellObservedData(object):
    """An iterable collection of :class:`cegalprizm.pythontool.ObservedData` objects, representing
    the observed data for an ObservedDataSet."""

    def __init__(self, observed_data_set: "ObservedDataSet"):
        self._observed_data_set = observed_data_set

    def __iter__(self) -> typing.Iterator[ObservedData]:
        for p in self._observed_data_set._get_observed_data_objects():
            yield p

    def __getitem__(self, idx: int) -> ObservedData:
        ods = list(self._observed_data_set._get_observed_data_objects())
        return ods[idx] # type: ignore

    def __len__(self) -> int:
        return self._observed_data_set._get_number_of_observed_data_objects()

    def __str__(self) -> str:
        return 'WellObservedData(observed_data_set="{0}"")'.format(self._observed_data_set)

    @property
    def readonly(self) -> bool:
        return self._observed_data_set.readonly

class ObservedDataSet(PetrelObject):
    """A class holding information about a observed data set"""

    def __init__(self, petrel_object_link: "ObservedDataSetGrpc"):
        super(ObservedDataSet, self).__init__(petrel_object_link)
        self._observeddataset_object_link = petrel_object_link

    def __str__(self) -> str:
        """A readable representation of the observed data set"""
        return 'ObservedDataSet(petrel_name="{0}")'.format(self.petrel_name)

    @property
    def well(self) -> "Well":
        """The parent well of the observed data set

        Returns:
            cegalprizm.pythontool.Well: The parent well of the observed data set
        """
        well = self._observeddataset_object_link.GetParentPythonBoreholeObject()
        return borehole.Well(well)

    @property
    def observed_data(self) -> WellObservedData:
        """An iterable collection of observed data objects for the ObservedDataSet
        
        Returns:
            cegalprizm.pythontool.observeddata.WellObservedData: the observed data for the observed data set"""
        return WellObservedData(self)

    @property
    def dates(self) -> typing.List[datetime.datetime]:
        """Returns a list of the Dates in this observed data set"""
        return [_utils.to_python_datetime(date) for date in self._observeddataset_object_link.GetDates()]

    def as_dataframe(self) -> pd.DataFrame:
        """Returns a dataframe containing the dates and observed data of this observed data set"""
        import pandas as pd
        df =  pd.DataFrame()
        df['Date'] = [_utils.to_python_datetime(date) for date in self._observeddataset_object_link.GetDates()]
        for observed_data in self.observed_data:
            values = observed_data._observed_data_object_link.GetValues()
            df[observed_data.petrel_name] = values
        return df
    
    def append_row(self, date: datetime.datetime, observed_data: typing.List[ObservedData], observed_data_values: typing.List[float]):
        """Append an entry to the end of this observed data set

        Args:
            date: the next date to append, new date must be greater than the the last date entry
            observed_data: the order of the observed data for the new observed_data_values
            observed_data_values: values to use for the new entry, order must match observed_data input

        Raises:
            PythonToolException: if input observed_data and observed_data_values count are not equal
        """
        if (len(observed_data) != len(observed_data_values)):
            raise PythonToolException('Input observed_data and observed_data_values must be of equal length')

        self._observeddataset_object_link.Append(_utils.from_python_datetime(date), tuple([od._observed_data_object_link for od in observed_data]), observed_data_values)

    def add_observed_data(self, global_observed_data_id: str, observed_data_values: typing.List[float]) -> ObservedData:
        """Add a new observed data for this observed data set

        Args:
            global_observed_data_id: the id for the global observed data to add to this observed data set
            observed_data_values: the list of observed data_values to set

        Returns:
            cegalprizm.pythontool.ObservedData: The newly created observed data object
        """        

        return ObservedData(self._observeddataset_object_link.CreateObservedData(global_observed_data_id, observed_data_values))

    def _get_observed_data_objects(self):
        for od in self._observeddataset_object_link.GetObservedDataObjects():
            od_py = ObservedData(od)
            yield od_py
    
    def _get_number_of_observed_data_objects(self) -> int:
        return self._observeddataset_object_link.GetNumberOfObservedDataObjects()

class ObservedDataSets(object):
    """An iterable collection of :class:`cegalprizm.pythontool.ObservedDataSet` objects, representing
    the observed data sets for a Well."""

    def __init__(self, well: "Well"):
        self._well = well

    def __iter__(self) -> typing.Iterator[ObservedDataSet]:
        for p in self._well._get_observed_data_sets():
            yield p

    def __getitem__(self, idx) -> ObservedDataSet:
        ods = list(self._well._get_observed_data_sets())
        return ods[idx] # type: ignore

    def __len__(self) -> int:
        return self._well._get_number_of_observed_data_sets()

    def __str__(self) -> str:
        return 'ObservedDataSets(well="{0}"")'.format(self._well)

    @property
    def readonly(self) -> bool:
        return self._well.readonly