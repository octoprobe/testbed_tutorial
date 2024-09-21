import logging
import pathlib

logger = logging.getLogger(__file__)

DIRECTORY_OF_THIS_FILE = pathlib.Path(__file__).parent


PYTEST_OPT_GIT_MICROPYTHON = "--git-micropython"
DEFAULT_GIT_MICROPYTHON = "https://github.com/micropython/micropython.git@master"
