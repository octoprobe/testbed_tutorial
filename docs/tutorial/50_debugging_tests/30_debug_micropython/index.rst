Debug on level micropython
==========================

.. note:: 

    Before every test, there should be NO micropython on the MCU. The Octoprobe session setup should take care of this.

    The test will then copy the micropython code to the MCU.

    Octoprobe uses `mpremote`` to communicate with the MCU.

    A test typically executed micropython code on the MCU.

    Later, the test will read variables from the MCU to verify if the test succeded or failed.


You might be used to debug micropython code with your favorite tool like thonny.

Octoprobe allows you to stop a test so you make take over using your favorite tool.

However, when the test has finished, the relays will opened. So we should not wait to the test do finish, instead we add this line of code:

.. code-block:: python

    @pytest.mark.required_futs(EnumFut.FUT_I2C)
    def test_i2c_pattern(mcu: Tentacle) -> None:
        """
        This tests creates pulses:
        trig1: 1ms
        trig2: 2ms
        data1: 3ms
        data2: 4ms

        Have a look at docs/schematics_kicad/schematics.pdf to find testpoints to measure with a scope.
        """
        assert mcu.is_mcu
        mcu_config = mcu.tentacle_spec.mcu_config
        mp_program = """
    from machine import Pin, I2C

    import sys
    if sys.platform == 'pyboard':
        from pyb import PWM
    else:
        from machine import PWM

    # 'trig1' triggers the DAQ. So we initialize it last!
    ticks_ms=int((2**16)/10)
    PWM(Pin('{{mcu_config.data2}}'), freq=100, duty_u16=4*ticks_ms)
    PWM(Pin('{{mcu_config.data1}}'), freq=100, duty_u16=3*ticks_ms)
    PWM(Pin('{{mcu_config.trig2}}'), freq=100, duty_u16=2*ticks_ms)
    PWM(Pin('{{mcu_config.trig1}}'), freq=100, duty_u16=1*ticks_ms)
    """
        mcu.dut.mp_remote.exec_render(mp_program, mcu_config=mcu_config)
        mcu.dut.inspection_exit()

Note the last line `mcu.dut.inspection_exit()`. This line will hard exit the test with this output:

.. code-block:: text

    Exiting without cleanup. You may now take over the MCU on port=/dev/ttyACM2

Now use user favorite tool like Thonny and connect to `/dev/ttyACM2`. You may use a scope to have a look at the signals.


.. note:: 

  You do not need to quit your tool to free `/dev/ttyACM2` before the next test run: Octoprobe will powercycle the MCU which will automatically disconnect it.
