# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.




import unittest
from hypothesis import strategies as st
from hypothesis import assume, given
from cegalprizm.pythontool._system import _system
from cegalprizm.pythontool._toolmode import _ToolMode
import numpy as np
import math
from functools import wraps

from cegalprizm.pythontool._type_converters import _TypeConverter

def inprocess(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        old_mode = _ToolMode._is_oop 
        _ToolMode._is_oop = False
        fn(*args, **kwargs)
        _ToolMode._is_oop = old_mode
    return wrapper


def get_np_net_pair(draw, strat, py_type, net_type):
    Sys = _system()
    ls = draw(strat)
    assume(len(ls) > 0)
    net_array = _system().Array.CreateInstance(Sys.Object, len(ls))
        
    for i, elm in enumerate(ls):
        net_array[i] = net_type(elm)

    return np.array(ls, dtype=py_type), net_array

def helper_convert_from_python_enumerable(arr_input, sys_expected):
    assert len(arr_input) == len(sys_expected)
    
    ls_sys_actual = _TypeConverter().convert_from_python_enumerable(arr_input, True)

    assert len(ls_sys_actual) == len(sys_expected)
    for a, e in zip(ls_sys_actual, sys_expected):
        if type(a) == str and a != e:
            print(a)
            print(e)
        assert a == e, f"'{a}' is not equal to the expected value '{e}', types are '{type(a)}' and '{type(e)}'"


@st.composite
def get_np_net_string_pair(draw):
    return get_np_net_pair(draw, st.lists(st.text()), np.str_, _system().String)

@inprocess
@given(pair_of_net_sys_lists=get_np_net_string_pair())
def test_convert_from_python_enumerable_string(pair_of_net_sys_lists):
    helper_convert_from_python_enumerable(*pair_of_net_sys_lists)


def helper_convert_from_python_enumerable_numbers(arr_input, sys_expected):
    assert len(arr_input) == len(sys_expected)
    
    ls_sys_actual = _TypeConverter().convert_from_python_enumerable(arr_input, True)

    assert len(ls_sys_actual) == len(sys_expected)
    for a, e in zip(ls_sys_actual, sys_expected):
        if np.isnan(e):
            if np.isnan(a):
                continue
            assert False, f"'{a}' is not nan like the expected value '{e}'"
        assert a == e, f"'{a}' is not equal to the expected value '{e}'"

@st.composite
def get_np_net_float32_pair(draw):
    return get_np_net_pair(draw, st.lists(st.floats()), np.float32, _system().Double)

@inprocess
@given(pair_of_net_sys_lists=get_np_net_float32_pair())
def test_convert_from_python_enumerable_float32(pair_of_net_sys_lists):
    helper_convert_from_python_enumerable_numbers(*pair_of_net_sys_lists)


@st.composite
def get_np_net_float64_pair(draw):
    return get_np_net_pair(draw, st.lists(st.floats()), np.float64, _system().Double)

@inprocess
@given(pair_of_net_sys_lists=get_np_net_float64_pair())
def test_convert_from_python_enumerable_float64(pair_of_net_sys_lists):
    helper_convert_from_python_enumerable_numbers(*pair_of_net_sys_lists)

@st.composite
def get_np_net_Single_pair(draw):
    return get_np_net_pair(draw, st.lists(st.floats()), np.float64, _system().Single)

@inprocess
@given(pair_of_net_sys_lists=get_np_net_Single_pair())
def test_convert_from_python_enumerable_Single(pair_of_net_sys_lists):
    helper_convert_from_python_enumerable_numbers(*pair_of_net_sys_lists)


@st.composite
def get_np_net_int32_pair(draw):
    return get_np_net_pair(draw, st.lists(st.integers(min_value=-2147483648, max_value=2147483647)), np.int32, _system().Int32)

@inprocess
@given(pair_of_net_sys_lists=get_np_net_int32_pair())
def test_convert_from_python_enumerable_int32(pair_of_net_sys_lists):
    helper_convert_from_python_enumerable_numbers(*pair_of_net_sys_lists)

@st.composite
def get_np_net_int64_pair(draw):
    return get_np_net_pair(draw, st.lists(st.integers(min_value=-2147483648, max_value=2147483647)), np.int64, _system().Int32)

@inprocess
@given(pair_of_net_sys_lists=get_np_net_int64_pair())
def test_convert_from_python_enumerable_int64(pair_of_net_sys_lists):
    helper_convert_from_python_enumerable_numbers(*pair_of_net_sys_lists)



@st.composite
def get_np_net_bool_pair(draw):
    return get_np_net_pair(draw, st.lists(st.booleans()), np.bool_, _system().Boolean)

@inprocess
@given(pair_of_net_sys_lists=get_np_net_bool_pair())
def test_convert_from_python_enumerable_bool(pair_of_net_sys_lists):
    helper_convert_from_python_enumerable(*pair_of_net_sys_lists)


def get_py_net_pair(draw, strat, net_type):
    Sys = _system()
    ls = draw(strat)
    net_array = _system().Array.CreateInstance(Sys.Object, len(ls))
        
    for i, elm in enumerate(ls):
        net_array[i] = net_type(elm)

    return ls, net_array

def helper_convert_to_python_enumerable(arr_input, sys_expected):
    assert len(arr_input) == len(sys_expected)
    
    ls_sys_actual = _TypeConverter().convert_to_python_enumerable(arr_input, True)

    assert len(ls_sys_actual) == len(sys_expected)
    for a, e in zip(ls_sys_actual, sys_expected):
        if np.isnan(e):
            if np.isnan(a):
                continue
            assert False, f"'{a}' is not nan like the expected value '{e}'"
        assert a == e, f"'{a}' is not equal to the expected value '{e}'"



def helper_convert_cycle(arr_input, sys_expected):
    assert len(arr_input) == len(sys_expected)
    
    ls_sys_actual = _TypeConverter().convert_from_python_enumerable(arr_input, True)

    assert len(ls_sys_actual) == len(sys_expected)
    for a, e in zip(ls_sys_actual, sys_expected):
        if np.isnan(e):
            if np.isnan(a):
                continue
            assert False, f"'{a}' is not nan like the expected value '{e}'"
        assert a == e, f"'{a}' is not equal to the expected value '{e}'"


if __name__ == '__main__':
    _ToolMode._is_oop = False
    # test_convert_from_python_enumerable_string()
    # test_convert_from_python_enumerable_Single()
    # test_convert_from_python_enumerable_float32()
    test_convert_from_python_enumerable_int32()
    test_convert_from_python_enumerable_int64()
    test_convert_from_python_enumerable_float64()
    test_convert_from_python_enumerable_bool()
