import logging
import sys

import pytest
from octoprobe.lib_tentacle import Tentacle
from octoprobe.util_cached_git_repo import CachedGitRepo
from octoprobe.util_pytest.util_resultdir import ResultsDir
from octoprobe.util_subprocess import subprocess_run

from testbed_constants import DIRECTORY_TESTRESULTS, EnumFut
from util_github_micropython_org import (
    DIRECTORY_MICROPYTHON_GIT,
    DIRECTORY_MICROPYTHON_GIT_TESTS,
    PYTEST_OPT_GIT_MICROPYTHON,
    git_micropython_target,
)

logger = logging.getLogger(__file__)

TIME_MIN_S = 60.0
TIME_H_S = 60.0 * TIME_MIN_S


@pytest.fixture(scope="session", autouse=True)
def clone_git_micropython(request: pytest.FixtureRequest) -> None:
    git_spec = request.config.getoption(PYTEST_OPT_GIT_MICROPYTHON)
    if git_spec is None:
        pytest.skip(
            "Micropython repo not cloned - argument '{PYTEST_OPT_GIT_MICROPYTHON}'not given to pytest !"
        )
    git = CachedGitRepo()
    if not git.clone(directory=DIRECTORY_MICROPYTHON_GIT, git_spec=git_spec):
        pytest.skip("Micropython repo not cloned!")


@pytest.mark.required_futs(EnumFut.FUT_MCU_ONLY)
def test_perf_bench(mcu: Tentacle, artifacts_directory: ResultsDir) -> None:
    """
    This tests runs: run-perfbench.py
    https://github.com/micropython/micropython/blob/master/tests/README.md
    https://github.com/micropython/micropython/blob/master/tests/run-perfbench.py
    """
    args = [
        sys.executable,
        "run-perfbench.py",
        "--pyboard",
        f"--device={mcu.dut.get_tty()}",
        "168",
        "100",
    ]
    stdout = subprocess_run(
        args=args,
        cwd=DIRECTORY_MICROPYTHON_GIT_TESTS,
        timeout_s=300.0,
    )
    artifacts_directory("run-perfbench.txt").filename.write_text(stdout)


@pytest.mark.required_futs(EnumFut.FUT_MCU_ONLY)
def test_tests(mcu: Tentacle, artifacts_directory: ResultsDir) -> None:
    """
    This tests runs: run-tests.py
    https://github.com/micropython/micropython/blob/master/tests/README.md
    https://github.com/micropython/micropython/blob/master/tests/run-tests.py
    """
    args = [
        sys.executable,
        "run-tests.py",
        f"--device={mcu.dut.get_tty()}",
        f"--target={git_micropython_target(mcu)}",
        "--jobs=1",
        f"--result-dir={DIRECTORY_TESTRESULTS}",
        "--test-dirs=misc",
        # "misc/cexample_class.py",
    ]
    stdout = subprocess_run(
        args=args,
        cwd=DIRECTORY_MICROPYTHON_GIT_TESTS,
        timeout_s=TIME_H_S,
    )
    artifacts_directory("run-tests.txt").filename.write_text(stdout)
