#!/bin/bash
while true
do
    pytest -v -s --firmware-build-url=https://github.com/micropython/micropython@master tests/test_simple.py::test_i2c

    # pytest -v -s tests/test_simple.py --firmware-json=pytest_args_firmware_RPI_PICO2_v1.24.0.json
    echo done $? >> test_forever.log
	sleep 1
done
