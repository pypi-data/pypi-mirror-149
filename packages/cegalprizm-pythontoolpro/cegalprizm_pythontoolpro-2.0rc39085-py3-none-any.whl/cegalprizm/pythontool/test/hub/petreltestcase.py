# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



from os import execv, read
import typing
import unittest
from cegalprizm.hub import Hub, client_config
import pathlib


class PetreltestUnitCase(unittest.TestCase):
    _project: typing.Optional[str] = None

    def setUp(self) -> None:
        super().setUp()
        # self._ptx.load_project(path = self._project, read_only=False)

    @classmethod
    def setUpClass(cls):
        client_config.ClientConfig().set_use_auth(True)
        if not cls._project:
             raise RuntimeError("self._project must be set by child class before running tests")
        cls._h = Hub()
        # cls._h.activate()
        cls._ptx = cls._h.default_petrel_ctx()
        try:
            if not pathlib.Path(cls._project) == pathlib.Path(cls._ptx.project_info().path):
                cls._ptx.load_project(path = cls._project, read_only=False)
        except Exception as e:
            cls._ptx.load_project(path = cls._project, read_only=False)