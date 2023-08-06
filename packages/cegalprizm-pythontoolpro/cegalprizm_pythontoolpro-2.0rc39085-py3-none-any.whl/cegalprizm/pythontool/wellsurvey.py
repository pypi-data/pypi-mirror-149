# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.




import typing
import pandas as pd
from cegalprizm.pythontool import PetrelObject
from cegalprizm.pythontool import exceptions
from cegalprizm.pythontool import borehole
if typing.TYPE_CHECKING:
    from cegalprizm.pythontool.grpc.wellsurvey_grpc import DxdytvdWellSurveyGrpc, ExplicitWellSurveyGrpc, MdinclazimWellSurveyGrpc, XyzWellSurveyGrpc, XytvdWellSurveyGrpc
    from cegalprizm.pythontool.borehole import Well

class WellSurvey(PetrelObject):
    """A class holding information about a well survey"""

    def __init__(self, petrel_object_link:  typing.Union["DxdytvdWellSurveyGrpc", "ExplicitWellSurveyGrpc", "MdinclazimWellSurveyGrpc", "XyzWellSurveyGrpc", "XytvdWellSurveyGrpc"]):
        super(WellSurvey, self).__init__(petrel_object_link)
        self._wellsurvey_object_link = petrel_object_link
        self._well_survey_type = petrel_object_link.GetOceanType()

    @property
    def record_count(self) -> int:
        """The number of records in this well survey"""
        return self._wellsurvey_object_link.RecordCount() # int

    def __str__(self) -> str:
        """A readable representation of the well survey"""
        return 'WellSurvey(petrel_name="{0}")'.format(self.petrel_name)

    @property
    def well(self) -> "Well":
        """The well to which this well survey belongs to

        Returns:
            cegalprizm.pythontool.Well: the well for this well survey"""
        well = self._wellsurvey_object_link.GetParentPythonBoreholeObject()
        return borehole.Well(well)

    @property
    def well_survey_type(self) -> str:
        """Returns the type of well survey
        
        Returns:
            'X Y Z survey' 
                or 'X Y TVD survey' 
                or 'DX DY TVD survey' 
                or 'MD inclination azimuth survey'
                or 'Explicit survey'
        """
        if (self._well_survey_type == "XyzTrajectory"):
            return "X Y Z survey"
        elif (self._well_survey_type == "XyTvdTrajectory"):
            return "X Y TVD survey"
        elif (self._well_survey_type == "DxDyTvdTrajectory"):
            return "DX DY TVD survey"
        elif (self._well_survey_type == "MDInclinationAzimuthTrajectory"):
            return "MD inclination azimuth survey"
        elif (self._well_survey_type == "ExplicitTrajectory"):
            return "Explicit survey"
        else: 
            raise NotImplementedError("Cannot return the well_survey-type for this WellSurvey object")

    @property
    def azimuth_reference(self) -> str:
        """The azimuth reference for well survey types MD inclination azimuth survey and DX DY TVD survey 
    
        Returns:
            string: 'Grid north' or 'True north'

        Raises:
            PythonToolException: If the well survey is X Y Z well survey, X Y TVD well survey or Explicit survey
        """
        if (self._well_survey_type == "ExplicitTrajectory" or self._well_survey_type == "XyzTrajectory" or self._well_survey_type == "XyTvdTrajectory"):
            raise exceptions.PythonToolException("X Y Z well survey, X Y TVD well survey and Explicit survey have no azimuth reference.")
        return "Grid north" if self._wellsurvey_object_link.AzimuthReferenceIsGridNorth() else "True north" # type: ignore

    def set_survey_as_definitive(self):
        """Set well survey as definitive"""
        self._wellsurvey_object_link.SetSurveyAsDefinitive()

    def __is_lateral(self):
        return self._wellsurvey_object_link.IsLateral() # bool

    @property
    def tie_in_md(self) -> float:
        """Returns the tie-in MD point
        
        Raises:
            PythonToolException: If the well survey is not lateral
        """
        if (not self.__is_lateral()):
            raise exceptions.PythonToolException("WellSurvey is not lateral and therefore has no tie-in MD")

        tie_in_md = self._wellsurvey_object_link.TieInMd() # float
        return tie_in_md
    
    @tie_in_md.setter
    def tie_in_md(self, value: float):
        """Sets the tie-in MD for this well survey
        
        Raises:
            PythonToolException: If the well survey is not lateral
        """
        if (not self.__is_lateral()):
            raise exceptions.PythonToolException("WellSurvey is not lateral and therefore cannot set tie-in MD")

        ok = self._wellsurvey_object_link.SetTieInMd(value)

    def as_dataframe(self) -> pd.DataFrame:
        """The records of the well survey as a Pandas DataFrame

        The Ocean API limits what columns of the trajectory spreadsheet in Petrel are available to retrieve. The returned dataframe contains all possible columns.
        
        
        Returns:
            A Pandas DataFrame containing the available columns from the well survey spreadsheet
        """
        import numpy as np
        import pandas as pd

        if (self._well_survey_type == "XyzTrajectory"):
            # Default/editable records
            xs = [x for x in self._wellsurvey_object_link.GetXs()] 
            ys = [y for y in self._wellsurvey_object_link.GetYs()]
            zs = [z for z in self._wellsurvey_object_link.GetZs()]
            # Polyline/calculated records
            mds = [md for md in self._wellsurvey_object_link.GetMds()]
            incls = [incl for incl in self._wellsurvey_object_link.GetIncls()]
            azims = [azim for azim in self._wellsurvey_object_link.GetAzims()] # Azimuth values refer to grid north by default for XyzWellSurvey

            data = {"X": xs, "Y": ys, "Z": zs}
            if (len(xs) == len(mds)):
                data["MD"] = mds
            if (len(xs) == len(incls)):
                data["Inclination"] = incls
            if (len(xs) == len(azims)):
                data["Azimuth GN"] =azims

            return pd.DataFrame.from_dict(data)
        elif (self._well_survey_type == "XyTvdTrajectory"):
            # Default/editable records
            xs = [x for x in self._wellsurvey_object_link.GetXs()]
            ys = [y for y in self._wellsurvey_object_link.GetYs()]
            tvds = [tvd for tvd in self._wellsurvey_object_link.GetTvds()] # type: ignore

            # Polyline/calculated records
            zs = [z for z in self._wellsurvey_object_link.GetZs()]
            mds = [md for md in self._wellsurvey_object_link.GetMds()]
            incls = [incl for incl in self._wellsurvey_object_link.GetIncls()]
            azims = [azim for azim in self._wellsurvey_object_link.GetAzims()] # Azimuth values refer to grid north by default for XytvdWellSurvey

            data = {"X": xs, "Y": ys}
            if(len(xs) == len(zs)):
                data["Z"] = zs
            data["TVD"] = tvds
            if (len(xs) == len(mds)):
                data["MD"] = mds
            if (len(xs) == len(incls)):
                data["Inclination"] = incls
            if (len(xs) == len(azims)):
                data["Azimuth GN"] = azims

            return pd.DataFrame.from_dict(data)
        elif (self._well_survey_type == "DxDyTvdTrajectory"):
            # Default/editable records
            dxs = [dx for dx in self._wellsurvey_object_link.GetDxs()] # type: ignore
            dys = [dy for dy in self._wellsurvey_object_link.GetDys()] # type: ignore
            tvds = [tvd for tvd in self._wellsurvey_object_link.GetTvds()] # type: ignore

            # Polyline/calculated records
            xs = [x for x in self._wellsurvey_object_link.GetXs()] 
            ys = [y for y in self._wellsurvey_object_link.GetYs()]
            zs = [z for z in self._wellsurvey_object_link.GetZs()]
            mds = [md for md in self._wellsurvey_object_link.GetMds()]
            incls = [incl for incl in self._wellsurvey_object_link.GetIncls()]
            azims = [azim for azim in self._wellsurvey_object_link.GetAzims()] # Azimuth values refer to grid north by default for DxdytvdWellSurvey

            data = {}
            if (len(dxs) == len(xs)):
                data["X"] = xs
            if (len(dxs) == len(ys)):
                data["Y"] = ys
            if (len(dxs) == len(zs)):
                data["Z"] = zs
            data["DX"] = dxs
            data["DY"] = dys
            data["TVD"] = tvds
            if(len(dxs) == len(mds)):
                data["MD"] = mds
            if (len(dxs) == len(incls)):
                data["Inclination"] = incls
            if (len(dxs) == len(azims)):
                data["Azimuth GN"] = azims
            
            return pd.DataFrame.from_dict(data)
        elif (self._well_survey_type == "MDInclinationAzimuthTrajectory"):
            # Default/editable records
            mds = [md for md in self._wellsurvey_object_link.GetMds()]
            incls = [incl for incl in self._wellsurvey_object_link.GetIncls()]
            azims = [azim for azim in self._wellsurvey_object_link.GetAzims()]
            azim_head = "Azimuth GN" if (self._wellsurvey_object_link.IsAzimuthReferenceGridNorth()) else "Azimuth TN" # type: ignore

            # Polyline/calculated records
            xs = [x for x in self._wellsurvey_object_link.GetXs()] 
            ys = [y for y in self._wellsurvey_object_link.GetYs()]
            zs = [z for z in self._wellsurvey_object_link.GetZs()]

            data = {}
            if (len(mds) == len(xs)):
                data["X"] = xs
            if (len(mds) == len(ys)):
                data["Y"] = ys
            if (len(mds) == len(zs)):
                data["Z"] = zs
            data["MD"] = mds
            data["Inclination"] = incls
            data[azim_head] = azims

            return pd.DataFrame.from_dict(data)
        elif (self._well_survey_type == "ExplicitTrajectory"):
            mds = [md for md in self._wellsurvey_object_link.GetMds()]
            incls = [incl for incl in self._wellsurvey_object_link.GetIncls()]
            azims = [azim for azim in self._wellsurvey_object_link.GetAzims()]
            xs = [x for x in self._wellsurvey_object_link.GetXs()]
            ys = [y for y in self._wellsurvey_object_link.GetYs()]
            zs = [z for z in self._wellsurvey_object_link.GetZs()]
            data = {"X": xs,"Y": ys, "Z": zs,"MD": mds, "Inclination": incls, "Azimuth GN": azims}
            return pd.DataFrame.from_dict(data)
        else:
            raise NotImplementedError("WellSurvey type not implemented")

    def set(self,
            xs: typing.Optional[typing.List[float]]=None,
            ys: typing.Optional[typing.List[float]]=None,
            zs: typing.Optional[typing.List[float]]=None,
            dxs: typing.Optional[typing.List[float]]=None,
            dys: typing.Optional[typing.List[float]]=None,
            tvds: typing.Optional[typing.List[float]]=None,
            mds: typing.Optional[typing.List[float]]=None,
            incls: typing.Optional[typing.List[float]]=None,
            azims: typing.Optional[typing.List[float]]=None)\
            -> None:
        """
        Replaces all the records with the supplied arrays.

        For X Y Z survey - xs, ys, and zs is required as input
        
        For X Y TVD survey - xs, ys, tvds is required as input
        
        For DX DY TVD survey - dxs, dys and tvds is required as input
        
        For MD inclination azimuth - mds, incls and azims is required as input
        
        For Explicit survey - cannot modify records for well survey of type Explicit survey

        Args:
            xs: a list of x values
            ys: a list of y values
            zs: a list of z values
            dxs: a list of dx values
            dys: a list of dy values
            mds: a list of md values
            incls: a list of inclination values
            azims: a list of azimuth values

        Raises:
            PythonToolException: If the well survey is type Explicit survey or if WellSurvey is readonly
            ValueError: If the required input arrays are not provided or if they are of un-equal lengths
        """

        if (self._well_survey_type == "ExplicitTrajectory"):
            raise exceptions.PythonToolException("Cannot modify records for well survey of type Explicit survey")

        if (self.readonly):
            raise exceptions.PythonToolException("WellSurvey is readonly")

        if (self._well_survey_type == "XyzTrajectory"):
            if (xs is None or ys is None or zs is None):
                raise ValueError("Required input when setting records for X Y Z survey is xs, ys and zs")
            if (len(xs) != len(ys) != len(zs)):
                raise ValueError("Input arrays must have same length")
            self._wellsurvey_object_link.SetRecords(xs, ys, zs) # type: ignore

        elif (self._well_survey_type == "XyTvdTrajectory"):
            if (xs is None or ys is None or tvds is None):
                raise ValueError("Required input when setting records for X Y TVD survey is xs, ys and tvds")
            if (len(xs) != len(ys) != len(tvds)):
                raise ValueError("Input arrays must have same length")
            self._wellsurvey_object_link.SetRecords(xs, ys, tvds) # type: ignore

        elif (self._well_survey_type == "DxDyTvdTrajectory"):
            if (dxs is None or dys is None or tvds is None):
                raise ValueError("Required input when setting records for DX DY TVD survey is dxs, dys and tvds")
            if (len(dxs) != len(dys) != len(tvds)):
                raise ValueError("Input arrays must have same length")
            self._wellsurvey_object_link.SetRecords(dxs, dys, tvds) # type: ignore

        elif (self._well_survey_type == "MDInclinationAzimuthTrajectory"):
            if (mds is None or incls is None or azims is None):
                raise ValueError("Required input when setting records for MD inclination azimuth survey is mds, incls and azims")
            if (len(mds) != len(incls) != len(azims)):
                raise ValueError("Input arrays must have same length")

            ## TODO: Check if incls and azims are within correct degree range

            self._wellsurvey_object_link.SetRecords(mds, incls, azims) # type: ignore

        else:
            raise NotImplementedError("Cannot set records for this WellSurvey object")

    def clone(self, name_of_clone: str, copy_values: bool = False) -> "WellSurvey":
        """ Creates a clone of the Petrel object.

        The clone is placed in the same collection as the source object.
        A clone cannot be created with the same name as an existing Petrel object in the same collection.

        This is a Python Tool Pro function and is not available when running scripts in the editor integrated in Python Tool or in a workflow.
        
        Parameters:
            path_of_clone: Petrel name of the clone
            copy_values: Set to True if values shall be copied into the clone. Defaults to False.

        Returns:
            WellSurvey: The clone
            
        Raises:
            Exception: If there already exists a Petrel object with the same name
            ValueError: If name_of_clone is empty or contains slashes
        """
        return typing.cast("WellSurvey", self._clone(name_of_clone, copy_values = copy_values))

class WellSurveys(object):
    """An iterable collection of :class:`cegalprizm.pythontool.WellSurvey` objects, representing
    the well surveys for a Well."""

    def __init__(self, well: "Well"):
        self._well = well

    def __iter__(self) -> typing.Iterator[WellSurvey]:
        for p in self._well._get_well_surveys():
            yield p

    def __getitem__(self, idx) -> WellSurvey:
        ods = [item for item in self._well._get_well_surveys()]
        return ods[idx] # type: ignore

    def __len__(self) -> int:
        return self._well._get_number_of_well_surveys()

    def __str__(self) -> str:
        return 'WellSurveys(well="{0}")'.format(self._well)

    @property
    def readonly(self) -> bool:
        return self._well.readonly