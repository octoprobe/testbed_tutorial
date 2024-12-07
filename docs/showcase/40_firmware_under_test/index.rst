Firmware under test
===================

Download firmware under Test
----------------------------

The firmware has to be build on github or a local computer.

The parameter ``pytest --firmware-json=...`` may be used to specify a url where the download may be downloaded.

Only the MCU tentacles will be tested which match the firmware.

See also: :doc:`/introduction/30_flightlevel_pytest`

Source code of the firmware download:

.. autoproperty:: octoprobe.util_dut_programmers::FirmwareDownloadSpec.filename()
    :no-index:

Build firmware under Test
-------------------------

The parameter ``pytest --firmware-json=...`` may be used to specify a url where the download may be downloaded.

During the pytest session setup, the git repo will be cloned and the built.

Source code of the git clone:

.. autoclass:: testbed.util_firmware_mpbuild::CachedGitRepo()
    :no-index:

Source code of the build

.. automethod:: testbed.util_firmware_mpbuild::build_firmware()
    :no-index:
