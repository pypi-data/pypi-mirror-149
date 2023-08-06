# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



import typing
import pandas as pd
from cegalprizm.pythontool.experimental import experimental_method
from cegalprizm.pythontool import PetrelObject
from cegalprizm.pythontool import _utils
from cegalprizm.pythontool import exceptions
from cegalprizm.pythontool import welllog
from cegalprizm.pythontool.observeddata import ObservedDataSet, ObservedDataSets
from cegalprizm.pythontool.wellsurvey import WellSurvey, WellSurveys
from cegalprizm.pythontool import petrellink
from cegalprizm.pythontool._toolmode import _ToolMode
import collections
import datetime

if typing.TYPE_CHECKING:
    from cegalprizm.pythontool.grpc.borehole_grpc import BoreholeGrpc

class Well(PetrelObject):
    """A class holding information about a well.

    Trajectory information can be derived via a :class:`cegalprizm.pythontool.LogSamples` 
    - no direct trajectory information is maintained here."""

    def __init__(self, petrel_object_link: "BoreholeGrpc"):
        super(Well, self).__init__(petrel_object_link)
        self._borehole_object_link = petrel_object_link
    
    def __str__(self) -> str:
        """A readable representation"""
        return 'Well(petrel_name="{0}")'.format(self.petrel_name)

    @property
    def logs(self) -> "welllog.Logs":
        """A readonly iterable collection of the logs for the well

        Returns:
            cegalprizm.pythontool.Logs: the logs for the well"""
        return welllog.Logs(self)

    @property
    def observed_data_sets(self) -> ObservedDataSets:
        """A readonly iterable collection of the observed data sets for the well
        
        Returns:
            cegalprizm.pythontool.ObservedDataSets: the observed data sets for the well"""
        return ObservedDataSets(self)

    @property
    def surveys(self) -> WellSurveys:
        """A readonly iterable collection of the well surveys for the well
        
        Returns:
            cegalprizm.pythontool.WellSurveys: the well surveys for the well"""
        return WellSurveys(self)

    # cpython-only
    def logs_dataframe(self, 
            global_well_logs: typing.Union[typing.Union["welllog.WellLog", "welllog.DiscreteWellLog", "welllog.GlobalWellLog", "petrellink.DiscreteGlobalWellLogs", "petrellink.GlobalWellLogs"], typing.Iterable[typing.Union["welllog.WellLog", "welllog.DiscreteWellLog", "welllog.GlobalWellLog", "petrellink.DiscreteGlobalWellLogs", "petrellink.GlobalWellLogs"]]], 
            discrete_data_as: typing.Union[str, int] = "string")\
            -> pd.DataFrame:
            
        """Log data for the passed well logs or global well logs as a Pandas dataframe. 

        Returns the log data for the passed global well logs resampled onto consistent MDs.
        You can pass a single well log or global well log or many as a list.

        This method is only available in CPython.

        Args:
            global_well_logs: a single WellLog, DiscreteWellLog, GlobalWellLog, 
                or DiscreteGlobalWellLogs or a list of either of them
            discrete_data_as: A flag to change how discrete data is displayed. 
                'string' will cause discrete data tag to be returned as name
                or 'value' will cause discrete data tag to be returned as int. Defaults to 'string'

        Returns:
            pandas.DataFrame: a dataframe of the resampled continous logs

        Raises:
            ValueError: if the supplied objects are not WellLog, DiscreteWellLog, GlobalWellLog, or DiscreteGlobalWellLog
        """
        import pandas as pd
        import numpy as np
        from cegalprizm.pythontool import WellLog, GlobalWellLog, DiscreteWellLog, DiscreteGlobalWellLog

        if not isinstance(global_well_logs, collections.abc.Iterable):
            global_well_logs = [global_well_logs]
        
        if any(
            o
            for o in global_well_logs
            if not (isinstance(o, WellLog) or isinstance(o, GlobalWellLog) or isinstance(o, DiscreteWellLog) or isinstance(o, DiscreteGlobalWellLog))
        ):
            raise ValueError(
                "You can only pass in GlobalWellLogs, DiscreteGlobalWellLogs, WellLogs or DiscreteWellLogs"
            )

        cont_logs = [l for l in global_well_logs if isinstance(l, WellLog) or isinstance(l, GlobalWellLog)]
        cont_global_logs = [l.global_well_log if isinstance(l, WellLog) else l for l in cont_logs]

        disc_logs = [l for l in global_well_logs if isinstance(l, DiscreteWellLog) or isinstance(l, DiscreteGlobalWellLog)]
        disc_global_logs = [l.global_well_log if isinstance(l, DiscreteWellLog) else l for l in disc_logs]

        existing_global_logs = [l.global_well_log for l in self.logs]
        existing_global_log_droids = [log._petrel_object_link.GetDroidString() for log in existing_global_logs]
        compatible_cont_global_logs = self.__get_compatible_logs(existing_global_log_droids, cont_global_logs)
        compatible_disc_global_logs = self.__get_compatible_logs(existing_global_log_droids, disc_global_logs)

        if len(compatible_cont_global_logs) == 0 and len(compatible_disc_global_logs) == 0:
            return pd.DataFrame()

        log_data = self._borehole_object_link.GetLogs(tuple([gwl._petrel_object_link for gwl in compatible_cont_global_logs]), tuple([gwl._petrel_object_link for gwl in compatible_disc_global_logs]))
        
        column_names = [gwl.petrel_name for gwl in compatible_cont_global_logs] + [gwl.petrel_name for gwl in compatible_disc_global_logs] + ["MD", "TWT", "TVD"]
        df = pd.DataFrame.from_records(log_data, columns = column_names)

        cont_logs_len = len(compatible_cont_global_logs)
        for i in range(len(compatible_disc_global_logs)):
            df.iloc[:, [cont_logs_len + i]] = df.iloc[:, [cont_logs_len + i]].fillna(-9999)
            df.iloc[:, [cont_logs_len + i]] = df.iloc[:, [cont_logs_len + i]].replace({-1: -9999})
            if discrete_data_as == 'value':   
                df.iloc[:, [cont_logs_len + i]] = df.iloc[:, [cont_logs_len + i]].astype(int)
            if discrete_data_as == 'string':
                discrete_codes = None
                if isinstance(compatible_disc_global_logs[i], DiscreteGlobalWellLog):
                    log = compatible_disc_global_logs[i].log(self.petrel_name)
                    discrete_codes = log.discrete_codes
                if isinstance(compatible_disc_global_logs[i], DiscreteWellLog):
                    discrete_codes = compatible_disc_global_logs[i].discrete_codes
                if not discrete_codes is None:
                    discrete_codes[-9999] = 'UNDEF'
                    df.iloc[:, [cont_logs_len + i]] = df.iloc[:, [cont_logs_len + i]].replace(discrete_codes)
                df.iloc[:, [cont_logs_len + i]] = df.iloc[:, [cont_logs_len + i]].astype(object)
                 
        return df

    @experimental_method
    def md_to_xytime(self, md: typing.List[float])\
            -> typing.Tuple[typing.List[float], typing.List[float], typing.List[float]]:            
        """Converts a list of MD values to X, Y and Z (time)

        Args:
            md: List with MD values

        Returns:
            Returns a tuple([x], [y], [z]), where x is a list of x positions, 
                y is a list of y positions and z is a list of z (time) positions.
                Wells without time will return NaN values.
        """               
        lst_xs = []
        lst_ys = []
        lst_zs = []
        n = 1000
        for i in range(0, len(md), n):
            data = self._borehole_object_link.GetElevationTimePosition(md[i:i+n])
            lst_xs.append(data[0])
            lst_ys.append(data[1])
            lst_zs.append(data[2])
        d = ([x for xs in lst_xs for x in xs ], 
            [y for ys in lst_ys for y in ys ], 
            [z for zs in lst_zs for z in zs ])
        return d

    @experimental_method
    def md_to_xydepth(self, md: typing.List[float])\
            -> typing.Tuple[typing.List[float], typing.List[float], typing.List[float]]:
        """Converts a list of MD values to X, Y and Z (depth)

        Args:
            md: List with MD values

        Returns:
            Returns a tuple([x], [y], [z]), where x is a list of x positions, 
                y is a list of y positions and z is a list of z (depth) positions of the md values.
        """         
        import pandas as pd
        lst_xs = []
        lst_ys = []
        lst_zs = []
        n = 1000
        for i in range(0, len(md), n):
            data = self._borehole_object_link.GetTvdPosition(md[i:i+n])
            lst_xs.append(data[0])
            lst_ys.append(data[1])
            lst_zs.append(data[2])
        d = ([x for xs in lst_xs for x in xs ], 
            [y for ys in lst_ys for y in ys ], 
            [z for zs in lst_zs for z in zs ])
        return d

    def __get_compatible_logs(self, existing_droids, global_logs):
        compatible_logs = []
        if (len(global_logs) > 0):
            for log in global_logs:
                droid = log._petrel_object_link.GetDroidString()
                if droid in existing_droids:
                    compatible_logs.append(log)
        return compatible_logs

    def _get_observed_data_sets(self) -> typing.Iterator[ObservedDataSet]:
        for odset in self._borehole_object_link.GetObservedDataSets():
            if odset is None:
                continue
            ods = ObservedDataSet(odset)
            yield ods

    def _get_number_of_observed_data_sets(self) -> int:
        return self._borehole_object_link.GetNumberOfObservedDataSets()

    def _get_well_surveys(self):
        xyz = self._get_xyz_well_surveys()
        xytvd = self._get_xytvd_well_surveys()
        dxdytvd = self._get_dxdytvd_well_surveys()
        mdinclazim = self._get_mdinclazim_well_surveys()
        explicit = self._get_explicit_well_surveys()
        return xyz + xytvd + dxdytvd + mdinclazim + explicit

    def _get_number_of_well_surveys(self) -> int:
        return self._borehole_object_link.GetNumberOfWellSurveys()

    def _get_xyz_well_surveys(self):
        return [WellSurvey(ws) for ws in self._borehole_object_link.GetXyzWellSurveys()]

    def _get_xytvd_well_surveys(self):
        return [WellSurvey(ws) for ws in self._borehole_object_link.GetXytvdWellSurveys()]

    def _get_dxdytvd_well_surveys(self):
        return [WellSurvey(ws) for ws in self._borehole_object_link.GetDxdytvdWellSurveys()]

    def _get_mdinclazim_well_surveys(self):
        return [WellSurvey(ws) for ws in self._borehole_object_link.GetMdinclazimWellSurveys()]
        
    def _get_explicit_well_surveys(self):
        return [WellSurvey(ws) for ws in self._borehole_object_link.GetExplicitWellSurveys()]
