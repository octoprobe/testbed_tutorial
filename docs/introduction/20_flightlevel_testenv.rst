
Flightlevel: testbed
==============================================================================================

.. note:: 

    This section explains:

    * How a *testbed* is configured.
    * How a *testbed instance* is configured.

Tests always run against a specific `testbed`. See: :doc:`/testbed_showcase/index`.

This secion is about specifying such a testbed.

Specification of the testbed
---------------------------------------------------------------

.. rubric:: Supported **FUTS**

File: src/testbed/constants.py

.. code-block:: python
   :linenos:

   class EnumFut(enum.StrEnum):
      FUT_MCU_ONLY = enum.auto()
      FUT_I2C = enum.auto()
      FUT_UART = enum.auto()
      FUT_ONEWIRE = enum.auto()
      FUT_TIMER = enum.auto()

.. rubric::  Tentacle Types

File: src/testbed/constants.py

.. code-block:: python
   :linenos:

   class TentacleType(enum.StrEnum):
      TENTACLE_MCU = enum.auto()
      TENTACLE_DEVICE_POTPOURRY = enum.auto()
      TENTACLE_DAQ_SALEAE = enum.auto()


Configure the tentacles
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

File: src/testbed/tentacles_spec.py

.. code-block:: python
   :linenos:

   @dataclasses.dataclass
   class McuConfig:
      trig1: str
      trig2: str
      data1: str
      data2: str
      i2c: str
      onewire: str

The micropython code running on the MCUs differs from device to device - for example which GPIO to be used. See the use of this class in :doc:`40_flightlevel_micropython`.

File: src/testbed/tentacle_specs.py

.. code-block:: python
   :linenos:

   tentacle_spec_mcu_rpi_pico2 = TentacleSpec(
      tentacle_type=TentacleType.TENTACLE_MCU,
      futs=[
         EnumFut.FUT_MCU_ONLY,
         EnumFut.FUT_I2C,
         EnumFut.FUT_UART,
         EnumFut.FUT_ONEWIRE,
         EnumFut.FUT_TIMER,
      ],
      category="MicroPython Board",
      label="pico2",
      doc=DOC_TENTACLE_RPI_PICO2,
      mcu_usb_id=util_mcu_rp2.RPI_PICO2_USB_ID,
      tags="boards=RPI_PICO2:RPI_PICO2-RISCV,mcu=rp2,programmer=picotool",
      relays_closed={
         EnumFut.FUT_MCU_ONLY: [],
         EnumFut.FUT_I2C: [2, 3, 4, 5],
         EnumFut.FUT_ONEWIRE: [2, 3, 4],
      },
      mcu_config=McuConfig(
         trig1="GP20",
         trig2="GP21",
         data1="GP19",
         data2="GP18",
         i2c="i2c = I2C(1, scl=Pin('GP19'), sda=Pin('GP18'), freq=100_000)",
         onewire="GP14",
      ),
   )

* Line 2: It is a TENCALE_MCU
* Line 3: These *FUTS* are supported: *MCU_ONLY*, *I2C*, *UART*, *ONEWIRE* and *TIMER*.
* Line 14: `boards=RPI_PICO2:RPI_PICO2-RISCV`: Two firmware variants are supported `RPI_PICO2` and `RPI_PICO2-RISCV`
* Line 14: `mcu=rp2` the processor helps octoprobe to find the corresponding USB manufacturer/device id.
* Line 14: `programmer=picotool` specifies the programmer to be used.
* Line 17: `EnumFut.FUT_I2C: [2, 3, 4, 5],`: When a test specifies to test I2C, then octoprobe
  will close the relais `[2, 3, 4, 5]`.
  This information corresponds to the schematics of the tentacle.
* Line 21: `trig1="GP20",`: This fragment will be injected into micropython code. See :doc:`40_flightlevel_micropython`.

Configure of the testbed-instance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* A *testbed* is the specification of how the tentacles are populated and wired and how to test the different FUT.

  * Testbed/Tentacle specification

    * src/testbed/tentacle_spec_mcuconfig.py
    * src/testbed/tentacles_spec.py

* A *testbed* may be instanciated (pysically assembled and soldered)
  serveral times:
  The same testbed may run in Switzerland with MCUs Pico and
  pyboard and also in Australia using MCUs Esp32, esp8266
  and Arduino Portenta C33.


* Tentacles inventory

.. literalinclude:: ../../src/testbed/tentacles_inventory.py
   :language: python
   :linenos:
