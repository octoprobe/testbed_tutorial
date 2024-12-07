Write pytests
=============

If you are new to pytest, I recommend you to learn pytest without the complexity of Octoprobe.

Just start with the examples from https://docs.pytest.org/en/stable/how-to/index.html.

You might be interested in

* fixtures
* test collection (``--collect-only``)
* How to read pytest output (specially the ``-s`` flag.)
* The pytest explorer in VSCode
* How to debug pytests in VSCode


Setup and Teardown
------------------

The hardware has to be prepared for the tests. This is done by pytest before/after entering the tests.

For the example below, two MCU tentacles with PYBv1.1 and Pico are connected and started with this command:

.. code:: 

   pytest tests/test_simple.py::test_i2c tests/test_simple.py::test_onewire


.. mermaid::

   sequenceDiagram
      participant pytest
      participant test_i2c as Test I2C
      participant test_onewire as Test onewire
      participant pyb as Tentacle PYBv1.1
      participant pico as Tentacle Pico

      Note over pytest,pico: Setup SESSION

      pytest -) pytest: test collection: Which tentacles/MCU shall be tested?

      pytest -) pytest: git clone micropython, build firmware for required tentacles

      pytest -) pyb: Install firmware, Power off

      pytest -) pico: Install firmware, Power off 

      Note over pytest,pico: Test I2C on PYBv1.1

      pytest ->>+ pyb: Function-Setup: Power on
      pytest -) test_i2c: Run test I2C
      test_i2c -) pyb: Download and run I2C micropython code.

      pyb -->>- pytest: Function-Teardown: Power off

      Note over pytest,pico: Test Onewire on PYBv1.1

      pytest ->>+ pyb: Function-Setup: Power on
      pytest -) test_onewire: Run test Onewire
      test_onewire -) pyb: Download and run Onewire micropython code.

      pyb -->>- pytest: Function-Teardown: Power off

      Note over pytest,pico: Test I2C on Pico

      pytest ->>+ pico: Function-Setup: Power on
      pytest -) test_i2c: Run test I2C
      test_i2c -) pico: Download and run I2C micropython code.

      pico -->>- pytest: Function-Teardown: Power off

      Note over pytest,pico: Test Onewire on Pico

      pytest ->>+ pico: Function-Setup: Power on
      pytest -) test_onewire: Run test Onewire
      test_onewire -) pico: Download and run Onewire micropython code.

      pico -->>- pytest: Function-Teardown: Power off

      Note over pytest,pico: Teardown SESSION (does nothing)

Comments to above sequence diagram
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   
* SESSION setup

  * Will install the firmware and will power off all tentacles.

* FUNCTION setup:
    
  * Will power on the required tentacle.
  * Close the relais for the required tentalces.
  * Set the blue LED on.
  
* FUNCTION teardown:

  * Will power down the required tentacle.
  * Open the relais for the required tentalces.
  * Set the blue LED off.

References to to source code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Sessios setup: pytest fixture

  .. autofunction:: tests.conftest::session_setup
      :no-index:
  
* Sessios setup: Build the software

  .. autofunction:: testbed.util_firmware_mpbuild::build_firmwares()
      :no-index:

* Session setup: Install the firmware

  .. automethod:: octoprobe.octoprobe::NTestRun.function_setup_dut()
      :no-index:

  .. automethod:: octoprobe.octoprobe::NTestRun.function_setup_dut()
      :no-index:

* Function setup: pytest fixture

  .. autofunction:: tests.conftest::setup_tentacles()
      :no-index:

* Function setup: Set the relays

  .. automethod:: octoprobe.octoprobe::NTestRun.setup_relays
      :no-index:


* The test functions
  
  .. autofunction:: tests.test_simple::test_i2c()
      :no-index:

  .. autofunction:: tests.test_simple::test_onewire()
      :no-index:

