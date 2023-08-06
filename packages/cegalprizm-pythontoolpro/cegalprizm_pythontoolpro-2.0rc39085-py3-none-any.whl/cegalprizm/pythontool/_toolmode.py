# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



import inspect
import sys
import os
import typing
class _ToolMode:
    _is_oop: typing.Optional[bool] = None

    @staticmethod
    def is_ironpy() -> bool:
        return sys.version_info.major == 2

    @staticmethod
    def is_cpy() -> bool:
        return sys.version_info.major > 2 and not _ToolMode.is_oop()

    @staticmethod 
    def is_oop() -> bool:        
        if _ToolMode._is_oop == None:
            _ToolMode._is_oop = _ToolMode._find_mode()            

        return _ToolMode._is_oop # type: ignore

    @staticmethod
    def _find_mode() -> bool:
        if os.getenv('BLUEBACK_PYTHONTOOL_MODE') == 'in process':
            return False

        if sys.version_info[0] < 3:
            return False

        for frame in inspect.stack():
            if '\\sphinx\\ext\\autodoc\\' in frame.filename:
                return False

        if '\\pydist.zip\\' in inspect.stack()[0].filename:
            return False

        return True

    