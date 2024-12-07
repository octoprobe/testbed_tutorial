Debug on level hardware
=======================

Checklist to track down hardware problems

* Does the tentacle work correctly, in one case, a opto relays had cold solder joint.
* Are all relays close as expected?
* Are all relays of the tentacles which are not involved open?
* Are the connections on the tentacles soldered correctly.
* Is the micropython code working as expected.

Strategy to track down hardware problems
------------------------------------------

Remove all tentacles which are not invovled
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

 * Physically remove the tentacles.
 * Remove the tentacle from the configuration in `src/testbed/testbed_ch_wetzikon_1.py`.

Verify the relays
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    @pytest.mark.required_futs(EnumFut.FUT_I2C)
    def test_i2c_pattern(mcu: Tentacle) -> None:
        mcu.dut.inspection_exit()

Add `mcu.dut.inspection_exit()` just after the test starts. This ensures, that the relays of all tentacles involved are set correctly.

Now use a ohmmeter to verify the connections from end to end (For example MCU pin to I2c device pin).

Verify you python code using Thonny
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

With the relays still set correctly, use your favorite micropython tool (Thonny?) and download the micropython testcode.

Take a ohmmeter or scope to follow the signals.


Start moving micropython code into the test
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    @pytest.mark.required_futs(EnumFut.FUT_I2C)
    def test_i2c_pattern(mcu: Tentacle) -> None:
        mp_program = """
        from machine import Pin, I2C, PWM

        ticks_ms=int((2**16)/10)
        PWM(Pin('GP18'), freq=100, duty_u16=4*ticks_ms)
        PWM(Pin('GP17'), freq=100, duty_u16=3*ticks_ms)
        """
        mcu.dut.mp_remote.exec_render(mp_program, mcu_config=mcu_config)
        mcu.dut.inspection_exit()

Now some python code is downloaded to the MCU before `mcu.dut.inspection_exit()` was called.

Run the test and verify the signals with the scope.


.. note:: 

    You may stop your test in the VSCode debugger and verify the signals with the scope. But the serial line to the MCU will be still be locked by the test!

    However, `mcu.dut.inspection_exit()` will allow you to use serial line to the MCU. 
