from .tentacles_spec import EnumTentacleSpec

TENTACLES_INVENTORY: dict[str, str] = {
    # testbed_ch_wetzikon_1
    "e46340474b174429": EnumTentacleSpec.MCU_PYBV11,
    "e46340474b4e1831": EnumTentacleSpec.MCU_RPI_PICO2,
    "e46340474b4c1331": EnumTentacleSpec.DAQ_SALEAE,
    "e46340474b4c3f31": EnumTentacleSpec.DEVICE_POTPOURRY,
    # testbed_ch_greenliff_1
    "e46340474b551722": EnumTentacleSpec.MCU_RPI_PICO,
    "e46340474b164d29": EnumTentacleSpec.DAQ_SALEAE,
    "e46340474b574722": EnumTentacleSpec.DEVICE_POTPOURRY,
    # testbed_au_melbourne_1
    "e46340474b4c2731": EnumTentacleSpec.MCU_RPI_PICO2,
    "e46340474b283623": EnumTentacleSpec.DAQ_SALEAE,
    "e46340474b0c3523": EnumTentacleSpec.DEVICE_POTPOURRY,
    # testbed_au_melbourne_2
    "e46340474b141c29": EnumTentacleSpec.MCU_RPI_PICO2,
    "e46340474b121931": EnumTentacleSpec.DAQ_SALEAE,
    "e46340474b563b21": EnumTentacleSpec.DEVICE_POTPOURRY,
}
