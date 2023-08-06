# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



import collections
import numpy as np

class System:
    Minmax = collections.namedtuple('Minmax', ['MinValue', 'MaxValue'])
    Int32 = Minmax(int(-2147483648), int(2147483647))
    
    Nan = collections.namedtuple('Nan', 'NaN')
    Double = Nan(np.nan)

    class Array:
        @classmethod
        def CreateInstance(cls, element_type, number_of_elements):
            if element_type == int:
                return [int(0)] * number_of_elements
            if element_type == bool:
                return [False] * number_of_elements
            else:
                return [float(0)] * number_of_elements

