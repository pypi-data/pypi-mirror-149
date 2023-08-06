# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



from cegalprizm.pythontool.exceptions import PythonToolException
from functools import wraps

allow_experimental = False

def set_experimental_ok(b):
    global allow_experimental
    allow_experimental = b

def experimental_method(func):
    @wraps(func)
    def wrapped_func(*args, **kwargs):
        global allow_experimental
        if not allow_experimental:
            raise PythonToolException("Experimental methods must be explicitly allowed")
        return func(*args, **kwargs)

    if hasattr(func, "__doc__") and func.__doc__:
        wrapped_func.__doc__ = "EXPERIMENTAL METHOD!\n" + func.__doc__
    else:
        wrapped_func.__doc__ = "EXPERIMENTAL METHOD!"

    return wrapped_func
        
def experimental_class(cls):
    for attr_name in cls.__dict__:
        attr = getattr(cls, attr_name)
        if callable(attr):
            setattr(cls, attr_name, experimental_method(attr))

    if hasattr(cls, "__doc__") and cls.__doc__:
        cls.__doc__ = "EXPERIMENTAL CLASS!\n" + cls.__doc__
    else:
        cls.__doc__ = "EXPERIMENTAL CLASS!"

    return cls