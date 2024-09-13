Testsbeds produced
==================

Delivery Inspection
-------------------

Goal: Make sure that all tentacles work

Steps
* Connect all tentacles
* Run the tests, but update `OCTOPROBE_TESTBED`:
  
.. code:: 

    export OCTOPROBE_TESTBED=testbed_ch_wetzikon_1.py
    pytest -v -s tests/test_simple.py --firmware-json=pytest_args_firmware_RPI_PICO_v1.23.0.json


testbed_ch_wetzikon_1.py
------------------------
