# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.




from cegalprizm.pythontool._toolmode import _ToolMode
try:
    from cegalprizm.pythontool.ooponly.ptutils import System as oop_system
except:
    pass

_sys = None
def _system():
    global _sys
    if not _ToolMode.is_oop():
        if _sys:
            return _sys
        import clr # type: ignore
        import System # type: ignore
        _sys = System
        return _sys
    else:
        return oop_system
