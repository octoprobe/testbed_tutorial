from __future__ import annotations

from octoprobe.lib_tentacle import Tentacle
from octoprobe.lib_testbed import Testbed

from testbed_constants import EnumFut, TentacleType

from .testbed_tentacles import (
    McuConfig,
    tentacle_spec_daq_saleae,
    tentacle_spec_device_potpourry,
    tentacle_spec_pyboard,
    tentacle_spec_raspberry_pico,
)

tentacle_mcu_pyboard = Tentacle[McuConfig, TentacleType, EnumFut](
    tentacle_serial_number="e46340474b174429",
    tentacle_spec=tentacle_spec_pyboard,
)
tentacle_mcu_raspberry_pico = Tentacle[McuConfig, TentacleType, EnumFut](
    tentacle_serial_number="e46340474b551722",
    tentacle_spec=tentacle_spec_raspberry_pico,
)
tentacle_daq_saleae = Tentacle[McuConfig, TentacleType, EnumFut](
    tentacle_serial_number="e46340474b4c1331",
    tentacle_spec=tentacle_spec_daq_saleae,
)
tentacle_device_potpourry = Tentacle[McuConfig, TentacleType, EnumFut](
    tentacle_serial_number="e46340474b4c3f31",
    tentacle_spec=tentacle_spec_device_potpourry,
)


TESTBED = Testbed(
    workspace="ch_wetzikon_1",
    tentacles=[
        tentacle_mcu_pyboard,
        tentacle_mcu_raspberry_pico,
        tentacle_device_potpourry,
        tentacle_daq_saleae,
    ],
)
