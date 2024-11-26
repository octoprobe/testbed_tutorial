import logging
import pathlib

from mpbuild.board_database import Database
from mpbuild.build_api import build_by_variant_str
from octoprobe.lib_tentacle import Tentacle
from octoprobe.util_cached_git_repo import CachedGitRepo
from octoprobe.util_constants import TAG_BOARDS
from octoprobe.util_dut_programmers import FirmwareBuildSpec, FirmwareSpecBase
from octoprobe.util_micropython_boards import BoardVariant, board_variants

from .constants import DIRECTORY_GIT_CACHE

logger = logging.getLogger(__file__)


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

    logger.info(f"build firmware {variant.name_normalized} in {micropython_directory}")

    db = Database(micropython_directory)
    firmware = build_by_variant_str(
        db=db,
        variant_str=variant.name_normalized,
        do_clean=False,
    )
    return FirmwareBuildSpec(
        board_variant=BoardVariant(
            board=firmware.variant.board.name,
            variant=firmware.variant.name,
        ),
        _filename=firmware.filename,
        micropython_version_text=firmware.micropython_version_text,
    )


def build_firmwares(
    tentacles: list[Tentacle],
    collectonly: bool,
    firmware_git_url: str,
) -> list[FirmwareSpecBase]:
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

    firmware_specs: list[FirmwareSpecBase] = []
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
