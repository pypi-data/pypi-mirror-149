"""
TODO
"""

import logging
from typing import Type

from cppython.project import Project as CPPythonProject
from cppython.project import ProjectConfiguration
from cppython_core.schema import GeneratorDataType, Interface
from pdm import Core, Project
from pdm.models.candidates import Candidate
from pdm.signals import post_install


class CPPythonPlugin(Interface):
    """
    TODO
    """

    def __init__(self, core: Core) -> None:

        # NOTE: Verbosity is not filled
        self.configuration = ProjectConfiguration()
        self.configuration.verbosity = core.ui.verbosity
        self.project = None
        self.logger = logging.getLogger(__name__)

        post_install.connect(self.on_post_install, weak=False)

    def read_generator_data(self, generator_data_type: Type[GeneratorDataType]) -> GeneratorDataType:
        """
        TODO
        """
        return generator_data_type()

    def write_pyproject(self) -> None:
        """
        TODO:
        """

    def on_post_install(self, project: Project, candidates: dict[str, Candidate], dry_run: bool):
        """
        TODO
        """

        # Attach configuration for CPPythonPlugin callbacks
        self.project = project
        self.configuration.verbosity = bool(project.core.ui.verbosity)

        self.logger.info("CPPython: Entered 'on_post_install'")

        pdm_pyproject = project.pyproject

        if pdm_pyproject is None:
            self.logger.info("CPPython: Project data was not available")
            return

        cppython_project = CPPythonProject(self.configuration, self, pdm_pyproject)

        cppython_project.install()

    def register_logger(self, logger: logging.Logger) -> None:
        """
        TODO
        """
