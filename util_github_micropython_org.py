import logging
import pathlib
import sys

from octoprobe.lib_tentacle import Tentacle
from octoprobe.util_constants import TAG_BOARD

from testbed_constants import DIRECTORY_DOWNLOADS

logger = logging.getLogger(__file__)

DIRECTORY_OF_THIS_FILE = pathlib.Path(__file__).parent
DIRECTORY_MICROPYTHON_GIT = DIRECTORY_DOWNLOADS / "git_micropython"


DIRECTORY_MICROPYTHON_GIT_URL = DIRECTORY_MICROPYTHON_GIT.parent / "url.txt"
DIRECTORY_MICROPYTHON_GIT_TESTS = DIRECTORY_MICROPYTHON_GIT / "tests"
DIRECTORY_MICROPYTHON_GIT_TOOLS = DIRECTORY_MICROPYTHON_GIT / "tools"

PYTEST_OPT_GIT_MICROPYTHON = "--git-micropython"
DEFAULT_GIT_MICROPYTHON = "https://github.com/micropython/micropython.git@master"


def append_sys_path():
    """
    Append directories to the path
    """
    for subdir in DIRECTORY_MICROPYTHON_GIT_TESTS, DIRECTORY_MICROPYTHON_GIT_TOOLS:
        assert subdir.is_dir(), f"Directory missing: {subdir.absolute()}"
        sys.path.append(str(subdir))


def git_micropython_target(mcu: Tentacle) -> str:
    """
    The parameter: run-tests.py --target=rp2

    The target values are defined here: https://github.com/micropython/micropython/blob/master/tests/run-tests.py#L1116-L1158
    """
    board = mcu.get_property_mandatory(TAG_BOARD)

    dict_board_to_target = {
        "RPI_PICO": "rp2",
        "PYBV11": "pyboard",
    }

    try:
        return dict_board_to_target[board]
    except KeyError as e:
        raise KeyError(
            f"Unknown MCU '{board}: Expected one of {','.join(dict_board_to_target.keys())}"
        ) from e
