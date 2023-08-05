"""
TODO
"""
import pytest
from cppython.data import default_pyproject
from pdm import Core
from pytest_cppython.plugin import InterfaceUnitTests
from pytest_mock.plugin import MockerFixture

from cppython_pdm.plugin import CPPythonPlugin


class TestCPPythonInterface(InterfaceUnitTests):
    """
    The tests for the PDM interface
    """

    @pytest.fixture(name="interface")
    def fixture_interface(self) -> CPPythonPlugin:
        """
        Override of the plugin provided interface fixture.

        Returns:
            ConsoleInterface -- The Interface object to use for the CPPython defined tests
        """

        return CPPythonPlugin(Core())

    def test_install(self, interface: CPPythonPlugin, mocker: MockerFixture):
        """
        TODO
        """

        pdm_project = mocker.MagicMock()
        pdm_project.core.ui.verbosity = 0
        pdm_project.pyproject = dict(default_pyproject)

        interface.on_post_install(project=pdm_project, candidates={}, dry_run=False)

    def test_verbosity(self, interface: CPPythonPlugin, mocker: MockerFixture):
        """
        TODO
        """

        pdm_core = mocker.MagicMock()
        pdm_core.ui.verbosity = 1

        plugin = CPPythonPlugin(pdm_core)

        assert plugin.configuration.verbosity
