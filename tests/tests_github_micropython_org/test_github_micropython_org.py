import logging
import sys

import pytest
from octoprobe.lib_tentacle import Tentacle
from octoprobe.util_cached_git_repo import CachedGitRepo
from octoprobe.util_dut_mcu import TAG_MCU
from octoprobe.util_pytest.util_resultdir import ResultsDir
from octoprobe.util_subprocess import subprocess_run
from octoprobe.util_vscode_un_monkey_patch import un_monkey_patch

from testbed_constants import DIRECTORY_GIT_CACHE, EnumFut
from util_github_micropython_org import PYTEST_OPT_GIT_MICROPYTHON

logger = logging.getLogger(__file__)

GIT_REPO: CachedGitRepo | None = None


@pytest.fixture(scope="session", autouse=True)
def clone_git_micropython(request: pytest.FixtureRequest) -> None:
    """
    We have to clone the micropython git repo and use the tests from the subfolder "test".
    """
    git_spec = request.config.getoption(PYTEST_OPT_GIT_MICROPYTHON)
    if git_spec is None:
        pytest.skip(
            "Micropython repo not cloned - argument '{PYTEST_OPT_GIT_MICROPYTHON}'not given to pytest !"
        )

    global GIT_REPO
    GIT_REPO = CachedGitRepo(
        directory_cache=DIRECTORY_GIT_CACHE,
        git_spec=git_spec,
        prefix="micropython_tests_",
    )
    GIT_REPO.clone()

    # Avoid hanger in run-perfbench.py/run-tests.py
    un_monkey_patch()


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
        cwd=GIT_REPO.directory / "tests",
        timeout_s=300.0,
    )
    artifacts_directory("run-perfbench.txt").filename.write_text(stdout)


# @pytest.mark.parametrize("firmware_spec", ["aa", "bb"])
@pytest.mark.required_futs(EnumFut.FUT_MCU_ONLY)
def test_tests(mcu: Tentacle, artifacts_directory: ResultsDir) -> None:
    """
    This tests runs: run-tests.py
    https://github.com/micropython/micropython/blob/master/tests/README.md
    https://github.com/micropython/micropython/blob/master/tests/run-tests.py
    """
    # Synonyms: target, mcu, port!
    # This has to match with the firmware!!!
    target = mcu.get_tag_mandatory(TAG_MCU)

    args = [
        sys.executable,
        "run-tests.py",
        f"--device={mcu.dut.get_tty()}",
        f"--target={target}",
        "--jobs=1",
        f"--result-dir={artifacts_directory.directory_test}",
        "--test-dirs=misc",
        # "misc/cexample_class.py",
    ]
    stdout = subprocess_run(
        args=args,
        cwd=GIT_REPO.directory / "tests",
        timeout_s=60.0,
    )
    artifacts_directory("run-tests.txt").filename.write_text(stdout)
