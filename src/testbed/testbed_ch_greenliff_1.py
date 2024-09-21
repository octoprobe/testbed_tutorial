from __future__ import annotations

from octoprobe.lib_tentacle import Tentacle
from octoprobe.lib_testbed import Testbed

from testbed.constants import EnumFut, TentacleType
from testbed.tentacles_spec import (
    McuConfig,
    tentacle_spec_daq_saleae,
    tentacle_spec_device_potpourry,
    tentacle_spec_mcu_rpi_pico,
)

tentacle_mcu_rpi_pico = Tentacle[McuConfig, TentacleType, EnumFut](
    tentacle_serial_number="e46340474b551722",
    tentacle_spec=tentacle_spec_mcu_rpi_pico,
)
tentacle_daq_saleae = Tentacle[McuConfig, TentacleType, EnumFut](
    tentacle_serial_number="e46340474b164d29",
    tentacle_spec=tentacle_spec_daq_saleae,
)
tentacle_device_potpourry = Tentacle[McuConfig, TentacleType, EnumFut](
    tentacle_serial_number="e46340474b574722",
    tentacle_spec=tentacle_spec_device_potpourry,
)


TESTBED = Testbed(
    workspace="ch_greenliff_1",
    tentacles=[
        tentacle_mcu_rpi_pico,
        tentacle_device_potpourry,
        tentacle_daq_saleae,
    ],
)
