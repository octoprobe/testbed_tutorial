
Flightlevel: pytest
==============================================================================================

.. note:: 

    This section explains:

    * How to use pytest parameters to select the firmware to be tested.
    * How to run the different test suites.
    * How pytest selects tentacles and FUT (Feature Unter Test)
    * How pytest does testcollection.

    Required knowhow:

    *  `Pytest <https://docs.pytest.org/>`_


Be warned that pytest is quite a complex beast.
If you are not familiar with pytest, take time to read
a pytest tutorial about test collection and fixtures.
This time is a good investment as pytest is extremly powerful
and widely used.

.. note::

  All tests are located in the folder `<repo>/tests` !

pytest command line arguments
---------------------------------------------------------------

.. note:: 
  pytest already provides many command line arguments. This section is about the octoprobe specific command line arguments.
 
The arguments are implmented here:

.. autofunction:: tests.conftest.pytest_addoption()

.. code-block:: bash

  $ pytest --help
  ...
  --firmware-json=FIRMWARE_JSON
                        A json file specifying the firmware
  --firmware-build-url=FIRMWARE_BUILD_URL
                        The url to a git repo to be cloned and compiled
  --git-micropython=GIT_MICROPYTHON
                        The micropython repo to check out. Syntax https://github.com/micropython/micropython.git@master


Arguments `--firmware-json`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../pytest_args_firmware_RPI_PICO_v1.23.0.json
   :language: json
   :linenos:


`$ pytest --firmware-json=pytest_args_firmware_RPI_PICO_v1.23.0.json` will

* download the firmware (see *url* on line 3)
* Install this firmware an matching tentacles (see *board_variant* on line 2)
* Verify the installed version (see *micropython_version_text* on line 4)

Arguments `--firmware-build-url`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`$ pytest --firmware-build-url=https://github.com/dpgeorge/micropython.git@rp2-add-rp2350` will

* `git clone https://github.com/dpgeorge/micropython.git`
* `git checkout rp2-add-rp2350`
* Query the installed MCU tentacles for tags like `boards=RPI_PICO2:RPI_PICO2-RISCV`. From this the supported firmware / variants are collected.
* For every supported firmware / variant:
  
  * build the firmware using `mpbuild`
  * install the firmware
  * run the tests

Arguments `--git-micropython`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


`$ pytest --git-micropython=https://github.com/micropython/micropython.git@master` will

* `git clone https://github.com/micropython/micropython.git`
* `git checkout master`
* Run `tests/run-perfbench.py`

The pytest wrapper is implemented here:

.. autofunction:: tests.tests_github_micropython_org.test_github_micropython_org::test_perf_bench()
  :noindex:

pytest test collection
---------------------------------------------------------------

Pytest automatically collects tests.

.. code-block:: python
   :linenos:

    @pytest.mark.required_futs(EnumFut.FUT_I2C)
    def test_i2c(
        mcu: Tentacle,
        device_potpourry: Tentacle,
        daq_saleae: Tentacle,
    ) -> None:
      ...

Line 2: As `test_i2c(..)` starts with `test_`, it will be collected by pytest.
Line 3-5: This test requires 3 tentacles. The parameter names are reserved and match the tentacle type.
Line 1: This test will be testing `FUT_I2C`.

During testcollection pytest will:

* Collect all tests starting with `test_`
* Above `text_i2c()` will not be collected if

  * The connected testbed does not contain the required tentacle types.

* Above `text_i2c()` will be collected for
  
  * all combinations of tentacles matching the required tentacle types.
  * all firmware version supported by these mcu

.. rubric:: `pytest --collect-only -q` Will show the collected tests without executing them

.. code-block:: bash
   :linenos:

   $ pytest \
      --collect-only -q \
      --firmware-build-url=https://github.com/dpgeorge/micropython.git@rp2-add-rp2350 \
      tests/test_simple.py::test_i2c
    tests/test_simple.py::test_i2c[4429pyboard(PYBV11)-3f31potpourry-1331daq]
    tests/test_simple.py::test_i2c[4429pyboard(PYBV11-DP)-3f31potpourry-1331daq]
    tests/test_simple.py::test_i2c[4429pyboard(PYBV11-DP_THREAD)-3f31potpourry-1331daq]
    tests/test_simple.py::test_i2c[4429pyboard(PYBV11-THREAD)-3f31potpourry-1331daq]
    tests/test_simple.py::test_i2c[1831pico2(RPI_PICO2)-3f31potpourry-1331daq]
    tests/test_simple.py::test_i2c[1831pico2(RPI_PICO2-RISCV)-3f31potpourry-1331daq]
    ^^^^^^^^^^^^^^^^^^^^                                Filename of the test
                          ^^^^^^^^                      Testfunction
                                   ^^^^^^^^^^^^^^^^^^^^ '-' separated list of tentacles
                                                        assigned to the test

Above output lists all collected tests.

Line 3: `4429pyboard(PYBV11-DP)`: This is tentacle number *4429* which is a *pyboard*. The firmware under test is `PYBV11-DP` which stands for pyboard and double precision float.
Line 7: `1831pico2(RPI_PICO2-RISCV)`: This is tentacle number *1831* which is a *pico2*. The firmware under test is `RPI_PICO2-RISCV` which is the riscv version.

.. rubric:: The testcollection is implemented here:


.. autofunction:: tests.conftest::pytest_generate_tests()
  :noindex:


conftest.py
---------------------------------------------------------------

This file configures pytest and contains many important hooks.

.. rubric:: This function will setup and tear down octoprobe

.. autofunction:: tests.conftest::session_setup()
  :no-index:


.. rubric:: This function will setup and tear down the tentacles for every test

.. autofunction:: tests.conftest::setup_tentacles()
  :no-index:

testsuites
---------------------------------------------------------------

There are currently 3 *testsuites*:

* pytest: See `tests/test_simple.py`. These are tests purely written in pytest and serve as a best practice template.
* mictopython testsuite. See `tests/tests_github_micropython_org/test_github_micropython_org.py`. This will just start the tests `<micropython-repo>/tests/test_perf_bench.py`. I would propose to rewrite these test using purely pytest.
* pytest and mip: See `tests/test_mip.py`. This is a starting point for testing a *mip* or other mictopython libraries using octoprobe.
