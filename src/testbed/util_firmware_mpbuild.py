import logging
import pathlib

from mpbuild.board_database import Database
from mpbuild.build_api import build_by_variant_str
from octoprobe.lib_tentacle import Tentacle
from octoprobe.util_cached_git_repo import CachedGitRepo
from octoprobe.util_constants import TAG_BOARDS
from octoprobe.util_dut_programmers import FirmwareBuildSpec, FirmwareSpecBase
from octoprobe.util_micropython_boards import BoardVariant, board_variants

from testbed.constants import DIRECTORY_GIT_CACHE

logger = logging.getLogger(__file__)


class FirmwareBuilder:
    """
    It is difficult in pytest to keep track if git has
    already been cloned and if a firmware alread
    has been compiled.
    This class will build every variant only once, even if
    many tests might require it.
    """

    def __init__(self, firmware_git_url: str) -> None:
        self._already_build_firmwares: dict[str, FirmwareBuildSpec] = {}
        self.firmware_git_url = firmware_git_url
        self.git_repo = CachedGitRepo(
            directory_cache=DIRECTORY_GIT_CACHE,
            git_spec=firmware_git_url,
            prefix="micropython_firmware_",
        )
        self.git_repo.clone()

    def build_firmware(self, firmware_spec: FirmwareSpecBase) -> FirmwareBuildSpec:
        assert isinstance(firmware_spec, FirmwareBuildSpec)

        variant = firmware_spec.board_variant

        spec = self._already_build_firmwares.get(variant.name_normalized, None)
        if spec is None:
            spec = build_firmware(
                micropython_directory=self.git_repo.directory,
                variant=variant,
            )
        self._already_build_firmwares[variant.name_normalized] = spec
        return spec


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


def collect_firmware_specs(tentacles: list[Tentacle]) -> list[FirmwareSpecBase]:
    """
    Loops over all tentacles and finds
    the board variants that have to be
    build/downloaded.
    """
    set_variants: set[BoardVariant] = set()
    for tentacle in tentacles:
        if not tentacle.is_mcu:
            continue
        boards = tentacle.get_tag_mandatory(TAG_BOARDS)
        for variant in board_variants(boards):
            set_variants.add(variant)
    list_variants = sorted(set_variants, key=lambda v: v.name_normalized)

    return [
        FirmwareBuildSpec(board_variant=variant, micropython_version_text=None)
        for variant in list_variants
    ]
