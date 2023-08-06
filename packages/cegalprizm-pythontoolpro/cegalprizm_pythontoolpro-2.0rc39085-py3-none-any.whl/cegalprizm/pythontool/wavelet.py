# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.




from cegalprizm.pythontool.petrelobject import PetrelObject
from cegalprizm.pythontool.exceptions import PythonToolException
import numpy as np
import pandas as pd
import typing

if typing.TYPE_CHECKING:
    from cegalprizm.pythontool.grpc.wavelet_grpc import WaveletGrpc

class Wavelet(PetrelObject):
    """A class holding information about a wavelet"""
    def __init__(self, python_petrel_property:"WaveletGrpc"):
        super(Wavelet, self).__init__(python_petrel_property)
        self._wavelet_object_link = python_petrel_property

    @property
    def amplitudes(self) -> np.array:
        """ Returns the amplitudes of the wavelet object as a numpy array"""    
        amplitudes = [v for v in self._wavelet_object_link.Amplitudes()] # numpy.array[float]
        return np.array(amplitudes)

    @amplitudes.setter
    def amplitudes(self, values: typing.Iterable[float]) -> None:
        ok = self._wavelet_object_link.SetAmplitudes(values)

    @property
    def sample_count(self) -> int:
        """ The number of samples contained in the Wavelet object.

        returns:
            The number of points in the wavelet.

        """
        sample_count = self._wavelet_object_link.SampleCount() # int
        return sample_count

    @property
    def sampling_interval(self) -> float:
        sampling_interval = self._wavelet_object_link.SamplingInterval() # float
        return sampling_interval
    
    @sampling_interval.setter
    def sampling_interval(self, value: float) -> None:
        """ Returns the sampling rate of the wavelet object as a float"""
        if value <= 0:
            raise PythonToolException("Wavelet sampling interval must be positive")
        ok = self._wavelet_object_link.SetSamplingInterval(value) 

    @property
    def sampling_start(self) -> float:
        """ Returns the first time value of the wavelet object as a float"""
        sampling_start  = self._wavelet_object_link.SamplingStart() # float
        return sampling_start

    @sampling_start.setter
    def sampling_start(self, value: float) -> None:
        ok = self._wavelet_object_link.SetSamplingStart(value)

    @property
    def sample_points(self) -> "np.ndarray":
        """ Returns the time values of the wavelet object as a numpy array"""
        sample_points = [v for v in self._wavelet_object_link.SamplePoints()] # numpy.array[float]
        return np.array(sample_points)

    @property
    def time_unit_symbol(self) -> str:
        """Returns the time unit of the wavelet object"""        
        time_unit_symbol = self._wavelet_object_link.TimeUnitSymbol() # str
        return time_unit_symbol

    def as_dataframe(self) -> pd.DataFrame:
        """The values of the position and amplitude of the wavelet as a Pandas DataFrame"""
        positions = [v for v in self._wavelet_object_link.SamplePoints()] # numpy.array[float]
        amplitudes = [v for v in self._wavelet_object_link.Amplitudes()] # numpy.array[float]
        data = {'position': positions, 'amplitude': amplitudes}
        return pd.DataFrame.from_dict(data)  
    
    def set(self, amplitudes: typing.Iterable[float], 
            sampling_start: typing.Optional[float] = None, 
            sampling_interval: typing.Optional[float] = None) -> None:
        """Replaces all the wavelet amplitude with the supplied values

        Args:
            amplitudes: a list of the amplitude values
            sampling_start: the starting values of the wavelet. Defaults to None.
            sampling_interval: the sampling interval of the wavelet. Defaults to None.

        Raises:
            PythonToolException: Wavelet sampling interval must be positive
        """ 
        if sampling_interval and sampling_interval <= 0:
            raise PythonToolException("Wavelet sampling interval must be positive")
        
        ok = self._wavelet_object_link.SetAmplitudes(amplitudes)
        if sampling_start:
            ok &= self._wavelet_object_link.SetSamplingStart(sampling_start)
        
        if sampling_interval:
            ok &= self._wavelet_object_link.SetSamplingInterval(sampling_interval) 

    def __str__(self) -> str:
        return 'Wavelet(petrel_name="{0}")'.format(self.petrel_name)

    def clone(self, name_of_clone: str, copy_values: bool = False) -> "Wavelet":
        """ Creates a clone of the Petrel object.

        The clone is placed in the same collection as the source object.
        A clone cannot be created with the same name as an existing Petrel object in the same collection.

        This is a Python Tool Pro function and is not available when running scripts in the editor integrated in Python Tool or in a workflow.
        
        Parameters:
            path_of_clone: Petrel name of the clone
            copy_values: Set to True if values shall be copied into the clone. Defaults to False.

        Returns:
            Wavelet: The clone
            
        Raises:
            Exception: If there already exists a Petrel object with the same name
            ValueError: If name_of_clone is empty or contains slashes
        """
        return typing.cast("Wavelet", self._clone(name_of_clone, copy_values = copy_values))