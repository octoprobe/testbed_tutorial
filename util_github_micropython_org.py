import logging
import pathlib

from octoprobe.lib_tentacle import Tentacle
from octoprobe.util_constants import TAG_BOARD

logger = logging.getLogger(__file__)

DIRECTORY_OF_THIS_FILE = pathlib.Path(__file__).parent


PYTEST_OPT_GIT_MICROPYTHON = "--git-micropython"
DEFAULT_GIT_MICROPYTHON = "https://github.com/micropython/micropython.git@master"


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
