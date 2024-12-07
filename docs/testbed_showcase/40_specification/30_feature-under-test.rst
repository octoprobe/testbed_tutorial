Features under Test
===================


Feature under test `FUT_TIMER`
------------------------------

* Test proposals

  * Clock dividers, timers

    * stimuly: `TENTACLE_MCU` generates pulse or PWM on `SIGNAL_TRIGGER1/2`.
    * expected: `TENTACLE_DAQ_SALEAE` verifies this pulse.


Feature under test `FUT_I2C`
----------------------------

* Electrical setup

  * Exacly one `TENTACLE_MCU` connects to `SIGNAL_DATA1/2`.
  * Exactly one `TENTACLE_DEVICE_POTPOURRY` connects to `SIGNAL_DATA1/2`. This tentacle must provide the I2C pull ups.

* Test proposals

  * Datatransfer

    * stimuly: `TENTACLE_MCU` acts as a I2C-controller and the `TENTACLE_DEVICE_POTPOURRY` as a I2C-target.
    * expected: meaningful data

  * Errors

    * See comments below


Feature under test `FUT_UART`
-----------------------------

* Electrical setup

  * Exacly one `TENTACLE_MCU` connects to `SIGNAL_DATA1/2` and `SIGNAL_TRIGGER1/2`.

    * The TX pin of `TENTACLE_MCU` / `TENTACLE_DEVICE_POTPOURRY` requires a serial 1k resistor. This allows the `TENTACLE_DAQ_SALEAE` to destroy the signal.

  * Exactly one `TENTACLE_DEVICE_POTPOURRY` connects to `SIGNAL_DATA1/2`.

* Test proposals

  * Timing test sequence:

    * stimuly:

      * `TENTACLE_MCU`: `SIGNAL_TRIGGER1` low->high
      * `TENTACLE_MCU`: `SIGNAL_DATA1` send 3 characters
      * `TENTACLE_MCU`: `SIGNAL_TRIGGER1` high->low

    * expected:

      * This tests allows various timing aspects. For example [uart.flush()](https://github.com/micropython/micropython/issues/13377)

    * variants:

      * Test hardware UART vs software UART.
      * Test syncio vs asyncio.

  * Errors

    * See comments below

Feature under test `FUT_ONEWIRE`
--------------------------------

* Electrical setup

  * Exacly one `TENTACLE_MCU` connects to `SIGNAL_DATA1`.
  * Exactly one `TENTACLE_DEVICE_POTPOURRY` connects to `SIGNAL_DATA1`. This tentacle must provide the onewire pull up.

* Test proposals

  * OneWire scan without response

    * stimuly: `TENTACLE_MCU`: scan for sensors. No sensor is connected by opening the ONEWIRE relay and closing the I2C-SCL relay.
    * expected: No response after some timeout.

  * OneWire scan

    * stimuly: `TENTACLE_MCU`: scan for sensors.
    * expected: 2 sensors found.

  * OneWire communication

    * stimuly: `TENTACLE_MCU`: reads serial number from one sensors.
    * expected: serial number

  * OneWire communication with error

    * See comments below
  
Feature under test `FUT_I2C/FUT_UART/FUT_ONEWIRE`: Communication errors
-----------------------------------------------------------------------

* Test proposals

  * Recovering from errors

    * stimuly: I2C/UART/ONEWIRE communication. Now `TENTACLE_DAQ_SALEAE` tentacle overrides `SIGNAL_DATA1/2` to provoke errors.
    * expected: Error and recover.
    * challenge

      * How to introduce errors without introducing flakyness?
      * How to provoke data integrity errors (CRC)?
      * How to provoke protocol errors (timeouts, start/stop bit missing)?

How to electrically override `SIGNAL_DATA1/2`:

  * I2C/ONEWIRE: `SIGNAL_DATA1/2` are pulled up. `TENTACLE_DAQ_SALEAE` may just override these outputs.
  * UART: The TX-signals outputs have low impedance. A serial 1k resitor is added (see `TENTACLE_MCU_x`/`TENTACLE_DEVICE_x`) which then allows `TENTACLE_DAQ_SALEAE` to override both TX-signals.
