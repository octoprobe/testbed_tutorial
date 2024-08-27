import logging
import pathlib
import shutil
import time
from collections.abc import Iterator

import pytest
from octoprobe.lib_tentacle import Tentacle
from octoprobe.octoprobe import NTestRun
from octoprobe.util_dut_programmers import FirmwareSpec
from octoprobe.util_pytest import util_logging
from octoprobe.util_pytest.util_resultdir import ResultsDir
from octoprobe.util_pytest.util_vscode import break_into_debugger_on_exception
from pytest import fixture

from util_github_micropython_org import (
    DEFAULT_GIT_MICROPYTHON,
    PYTEST_OPT_GIT_MICROPYTHON,
)

from .testbed_ch_wetzikon_1 import TESTBED
from .testbed_constants import DIRECTORY_TESTRESULTS, EnumFut, TentacleType

logger = logging.getLogger(__file__)

DIRECTORY_OF_THIS_FILE = pathlib.Path(__file__).parent

DEFAULT_FIRMWARE_SPEC = (
    DIRECTORY_OF_THIS_FILE / "pytest_args_firmware_RPI_PICO_v1.22.1.json"
)
_PYTEST_OPT_FIRMWARE = "--firmware"


# Uncomment to following line
# to stop tests on exceptions
break_into_debugger_on_exception(globals())


def get_firmware_spec(config: pytest.Config) -> FirmwareSpec:
    assert isinstance(config, pytest.Config)

    firmware_spec_filename = config.getoption(_PYTEST_OPT_FIRMWARE)
    return FirmwareSpec.factory(filename=firmware_spec_filename)


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    print(metafunc.definition.nodeid)
    for marker in metafunc.definition.own_markers:
        print(f" {marker!r}")

    def get_marker(name: str) -> pytest.Mark:
        for marker in metafunc.definition.own_markers:
            if marker.name == name:
                return marker
        raise KeyError(f"Marker '{name}' not found!")

    def get_required_futs() -> list[EnumFut]:
        try:
            marker_required_futs = get_marker(name="required_futs")
        except KeyError:
            return []
        assert isinstance(marker_required_futs, pytest.Mark)
        return list(marker_required_futs.args)

    _required_futs = get_required_futs()
    for fut in _required_futs:
        assert EnumFut(fut), fut

    if "mcu" in metafunc.fixturenames:
        tentacles = TentacleType.TENTACLE_MCU.get_tentacles_for_type(
            tentacles=TESTBED.tentacles,
            required_futs=_required_futs,
        )
        firmware_spec = get_firmware_spec(config=metafunc.config)
        tentacles = list(filter(firmware_spec.match_board, tentacles))
        if len(tentacles) == 0:
            futs_text = ", ".join(f.name for f in _required_futs)
            msg = f"No tentacle where selected for testing. Required futs: {futs_text}"
            logger.warning(msg)
            pytest.skip(msg)

        def get_id(t: Tentacle) -> str:
            return t.pytest_id

        metafunc.parametrize("mcu", tentacles, ids=get_id)

    if "device_potpourry" in metafunc.fixturenames:
        tentacles = TentacleType.TENTACLE_DEVICE_POTPOURRY.get_tentacles_for_type(
            TESTBED.tentacles,
            required_futs=_required_futs,
        )
        assert len(tentacles) > 0
        metafunc.parametrize("device_potpourry", tentacles, ids=lambda t: t.pytest_id)

    if "daq_saleae" in metafunc.fixturenames:
        tentacles = TentacleType.TENTACLE_DAQ_SALEAE.get_tentacles_for_type(
            TESTBED.tentacles,
            required_futs=_required_futs,
        )
        assert len(tentacles) > 0
        metafunc.parametrize("daq_saleae", tentacles, ids=lambda t: t.pytest_id)


@pytest.fixture
def required_futs(request: pytest.FixtureRequest) -> list[EnumFut]:
    for m in request.node.own_markers:
        assert isinstance(m, pytest.Mark)
        if m.name == "required_futs":
            return list(m.args)
    return []


@pytest.fixture
def active_tentacles(request: pytest.FixtureRequest) -> list[Tentacle]:
    def inner() -> Iterator[Tentacle]:
        if not hasattr(request.node, "callspec"):
            return []
        for _param_name, param_value in request.node.callspec.params.items():
            if isinstance(param_value, Tentacle):
                yield param_value

    return list(inner())


@fixture(scope="session", autouse=True)
def testrun(request: pytest.FixtureRequest) -> Iterator[NTestRun]:
    if DIRECTORY_TESTRESULTS.exists():
        shutil.rmtree(DIRECTORY_TESTRESULTS, ignore_errors=False)
    DIRECTORY_TESTRESULTS.mkdir(parents=True, exist_ok=True)

    util_logging.init_logging()

    with util_logging.logs(DIRECTORY_TESTRESULTS):

        firmware_spec = get_firmware_spec(request.config)
        firmware_spec.download()
        _testrun = NTestRun(
            testbed=TESTBED,
            firmware_spec=firmware_spec,
        )

        _testrun.session_powercycle_tentacles()

        yield _testrun

    _testrun.session_teardown()


@fixture(scope="function", autouse=True)
def setup_tentacles(
    testrun: NTestRun,  # pylint: disable=W0621:redefined-outer-name
    required_futs: tuple[EnumFut],  # pylint: disable=W0621:redefined-outer-name
    active_tentacles: list[Tentacle],  # pylint: disable=W0621:redefined-outer-name
    artifacts_directory: ResultsDir,  # pylint: disable=W0621:redefined-outer-name
) -> Iterator[None]:
    if len(active_tentacles) == 0:
        # No tentacle has been specified: This is just a normal pytest.
        # Do not call setup/teardown
        yield
        return

    with util_logging.logs(artifacts_directory.directory_test):
        begin_s = time.monotonic()

        def duration_text(duration_s: float | None = None) -> str:
            if duration_s is None:
                duration_s = time.monotonic() - begin_s
            return f"duration={duration_s:0.1f}s"

        try:
            logger.info(
                f"TEST SETUP {artifacts_directory.test_nodeid} {duration_text(0.0)}"
            )
            testrun.function_prepare_dut()
            testrun.function_setup_infra()
            testrun.function_setup_dut(active_tentacles=active_tentacles)

            testrun.setup_relays(futs=required_futs, tentacles=active_tentacles)
            logger.info(
                f"TEST BEGIN {artifacts_directory.test_nodeid} {duration_text()}"
            )
            yield

        finally:
            logger.info(
                f"TEST TEARDOWN {artifacts_directory.test_nodeid} {duration_text()}"
            )
            try:
                testrun.function_teardown(active_tentacles=active_tentacles)
            except Exception as e:
                logger.exception(e)
            logger.info(f"TEST END {artifacts_directory.test_nodeid} {duration_text()}")


@pytest.fixture(scope="function")
def artifacts_directory(request: pytest.FixtureRequest) -> ResultsDir:
    """ """

    return ResultsDir(
        directory_top=DIRECTORY_TESTRESULTS,
        test_name=request.node.name,
        test_nodeid=request.node.nodeid,
    )


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        _PYTEST_OPT_FIRMWARE,
        action="store",
        default=str(DEFAULT_FIRMWARE_SPEC),
        help="A json file specifying the firmware",
    )
    parser.addoption(
        PYTEST_OPT_GIT_MICROPYTHON,
        action="store",
        default=None,
        help=f"The micropython repo to check out. Syntax {DEFAULT_GIT_MICROPYTHON}",
    )
