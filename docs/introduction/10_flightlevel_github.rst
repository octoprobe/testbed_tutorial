Flightlevel: github
===================

octoprobe may run as a selfhosted gitlab runner.
Tests may than be triggered by github actions.

Github runners will be selected by github by finding matching tags.

Tags of a github runner could be:

* octoprobe: A octoprobe runner!
* testbed_tutorial:  The testbed connected to the runner.
* MCU_PICO2, MCU_PYBV11: The connected mcu boards. This allows github to run tests on various runners if the support different MCUs.

Trigger testrun by PR (Pull Requst)
---------------------------------------------------------------

.. todo::

    Example of a github action which demonstrates to start tests on every PR.

Trigger testrun manually
---------------------------------------------------------------
.. todo::

    Example of a github action which allows to start tests manually.

    Parameters could be

    * Branch/PR
    * MCU/Firmware



Firmware build on Github
---------------------------------------------------------------
The firmware is build and stored somewhere in the web, for example `RPI_PICO-20240602-v1.23.0.uf2 <https://micropython.org/resources/firmware/RPI_PICO-20240602-v1.23.0.uf2>`_.

The url pointing to this firmware is passed to the runner.

The runner

* Install the firmware on the corresponding MCU tentacles
* Run the tests on that tentacles

.. todo::

    Proviede detailed github sample action

Firmware build by Octoprobe
---------------------------------------------------------------

A link to the micropython source repo is provided and the firmware is build on the runner.

The runner

* Clones the source repo
* Scans the MCU tentacles for supported firmware and variants.
* For every firmware and variant:
  
  * Compile the firmware using `mpbuild`
  * Install the firmware on the corresponding MCU tentacles
  * Run the tests on that tentacles

* Send the results back to github

.. todo::

    Proviede detailed github sample action
   