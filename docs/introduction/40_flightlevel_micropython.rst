
Flightlevel: micropython
==============================================================================================

.. note:: 

    This section explains:

    * How to execute micropython code on the MCU.
    * How to read results from the MCU.
    * How to render micropython code using jinja to make it portable between processor families.

    Required knowhow:

    *  `Jinja <https://jinja.palletsprojects.com/>`_

.. rubric:::: execute micropython code

File: tests/test_simple.py

.. code-block:: python
   :linenos:

    def test_i2c(
        mcu: Tentacle,
        device_potpourry: Tentacle,
        daq_saleae: Tentacle,
    ) -> None:
        mp_program = """
        from machine import Pin, I2C

        {{mcu_config.i2c}}

        pin_trigger_1 = Pin('{{mcu_config.trig1}}', mode=Pin.OUT, value=0)
        pin_trigger_2 = Pin('{{mcu_config.trig2}}', mode=Pin.OUT, value=0)
        pin_trigger_1.value(1)
        i2c_data = i2c.readfrom(0x50, 10, True)
        pin_trigger_1.value(0)
        """
        mcu.dut.mp_remote.exec_render(mp_program, mcu_config=mcu.tentacle_spec.mcu_config)

        i2c_data = mcu.dut.mp_remote.read_bytes("i2c_data")

* Line 1: `test_i2c()` is a pytest.
* Line 6-16: This is micropython code. The `{{..}}` fragments will be rendered by jinja.
* Line 11: If `mcu_config.trig1="GP20"`, then line will be rendered as `pin_trigger_1 = Pin('GP20', mode=Pin.OUT, value=0)`.
* Line 17: `mcu.dut.mp_remote.exec_render`: Execute the micropython code on the *dut* on the *mcu* tentacle.
* Line 17: `mcu_config=mcu.tentacle_spec.mcu_config` this will instruct jinja to replace `{{mcu_config.xyz}}` with the values of `mcu.tentacle_spec.mcu_config`. `mcu.tentacle_spec.mcu_config` is part of the tentacle specification. You can add new variables to `mcu.tentacle_spec.mcu_config` when ever needed.
* Line 28: Read the variable *i2c_data* from the *dut* on the *mcu* tentacle. The expected datatype is *bytes*.
