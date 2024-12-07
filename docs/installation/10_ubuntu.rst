Installation Ubuntu
===================

Target OS: Ubuntu Server 24.04.1 LTS.

To set up a Raspberry Pi 4/5, start with :doc:`20_raspberry`.

Installation: Users
-------------------

Octoprobe user: `octoprobe`
Github runner user: `githubrunner`

.. code::

    adduser octoprobe
    adduser githubrunner

Do not forget to config git:

.. code::

    git config --global user.name "Hans Maerki"
    git config --global user.email "buhtig.hans.maerki@ergoinfo.ch"


Installation: APT
-----------------

.. code::

    sudo apt update \
      && sudo apt upgrade -y \
      && sudo apt install -y git uhubctl dfu-util \
        python-is-python3 python3.12-venv \
        docker.io docker-buildx

    sudo groupadd docker
    sudo usermod -aG docker octoprobe
    sudo usermod -aG docker githubrunner

    sudo snap install astral-uv --classic


On Raspbian: Skip python3.12-venv


git clone testbed_showcase
--------------------------

.. code::

    git clone https://github.com/octoprobe/testbed_showcase.git

python
------

.. code::

    uv venv --python 3.13.0 ~/venv_octoprobe

    source ~/venv_octoprobe/bin/activate
    uv pip install -e ~/testbed_showcase

    echo 'source ~/venv_octoprobe/bin/activate' >> ~/.profile
    # Log out and in again

Software requiring root access
------------------------------

Will be used by mpremote and others

.. code::

    sudo usermod -a -G dialout octoprobe

.. code::

    op install

Now `op install` will instruct you to:

.. code::

    sudo chown root:root ~/octoprobe_downloads/binaries/aarch64/*
    sudo chmod a+s ~/octoprobe_downloads/binaries/aarch64/*
    echo 'PATH="$HOME/octoprobe_downloads/binaries/aarch64:$PATH"' >> ~/.profile
    


Run your first tests
--------------------

Connect tentacles:

* 1 tentacle_DAQ_SALEAE
* 1 tentacle_DEVICE_PORTPOURRY
* 1-n tentacle_MCU_xx

Start the tests

.. code:: 

   cd ~/testbed_showcase
   pytest --firmware-json=pytest_args_firmware_RPI_PICO2_v1.24.0.json tests/test_simple.py::test_i2c
