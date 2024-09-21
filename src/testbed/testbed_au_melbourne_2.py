from __future__ import annotations

from octoprobe.lib_tentacle import Tentacle
from octoprobe.lib_testbed import Testbed

from testbed.constants import EnumFut, TentacleType
from testbed.tentacles_spec import (
    McuConfig,
    tentacle_spec_daq_saleae,
    tentacle_spec_device_potpourry,
    tentacle_spec_mcu_rpi_pico2,
)

tentacle_mcu_rpi_pico2 = Tentacle[McuConfig, TentacleType, EnumFut](
    tentacle_serial_number="e46340474b4c2731",
    tentacle_spec=tentacle_spec_mcu_rpi_pico2,
)
tentacle_daq_saleae = Tentacle[McuConfig, TentacleType, EnumFut](
    tentacle_serial_number="e46340474b283623",
    tentacle_spec=tentacle_spec_daq_saleae,
)
tentacle_device_potpourry = Tentacle[McuConfig, TentacleType, EnumFut](
    tentacle_serial_number="e46340474b0c3523",
    tentacle_spec=tentacle_spec_device_potpourry,
)


TESTBED = Testbed(
    workspace="au_melbourne_2",
    tentacles=[
        tentacle_mcu_rpi_pico2,
        tentacle_device_potpourry,
        tentacle_daq_saleae,
    ],
)
