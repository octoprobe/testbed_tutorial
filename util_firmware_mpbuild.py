import os
import pathlib

from octoprobe.lib_tentacle import Tentacle
from octoprobe.util_cached_git_repo import CachedGitRepo
from octoprobe.util_constants import TAG_BOARDS
from octoprobe.util_dut_programmers import FirmwareBuildSpec
from octoprobe.util_micropython_boards import BoardVariant, board_variants

from testbed_constants import DIRECTORY_GIT_CACHE


def build_firmware(
    micropython_directory: pathlib.Path, variant: BoardVariant
) -> FirmwareBuildSpec:
    """
    This will compile the firmware

    Input: The git repo containing the micropython source
    Output: The filename of the compiled firmware.
    """
    assert isinstance(micropython_directory, pathlib.Path)
    assert isinstance(variant, BoardVariant)

    old_cwd = pathlib.Path.cwd()
    try:
        os.chdir(micropython_directory)
        from mpbuild.build import build_board
        from mpbuild.find_boards_hmaerki import Database

        db = Database()
        db_variant = db.get_variant(variant.board, variant.variant)
        firmware_filename = build_board(**db_variant.buildparams.as_named_parameters)
        return FirmwareBuildSpec(
            board_variant=variant,
            micropython_version_text=None,
            _filename=firmware_filename,
        )
    finally:
        os.chdir(old_cwd)


def build_firmwares(
    tentacles: list[Tentacle],
    collectonly: bool,
    firmware_git_url: str,
) -> list[FirmwareBuildSpec]:
    list_variants: list[BoardVariant] = []
    for tentacle in tentacles:
        if not tentacle.is_mcu:
            continue
        boards = tentacle.get_tag_mandatory(TAG_BOARDS)
        for variant in board_variants(boards):
            list_variants.append(variant)
    list_variants.sort(key=lambda v: v.name_normalized)

    if not collectonly:
        git_repo = CachedGitRepo(
            directory_cache=DIRECTORY_GIT_CACHE,
            git_spec=firmware_git_url,
            prefix="micropython_firmware_",
        )
        git_repo.clone()

    firmware_specs: list[FirmwareBuildSpec] = []
    for variant in list_variants:
        if collectonly:
            spec = FirmwareBuildSpec(
                board_variant=variant,
                micropython_version_text=None,
                _filename=pathlib.Path("dummy (collect-only)"),
            )
        else:
            spec = build_firmware(
                micropython_directory=git_repo.directory,
                variant=variant,
            )

        firmware_specs.append(spec)

    return firmware_specs
