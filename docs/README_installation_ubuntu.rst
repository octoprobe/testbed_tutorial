Installation Ubuntu
===================

Target OS: Ubuntu 24.04 LTS.

You may also set up a Raspberry Pi 4/5 as described here: [README_installation_raspberry.md](README_installation_raspberry.md)
And then continue with this guide.

Installation: Users
-------------------

Octoprobe user: `octoprobe`
Github runner user: `githubrunner`

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
    sudo usermod -aG docker $USER


On Raspbian: Skip python3.12-venv


## git clone testbed_tutorial

.. code::

    git clone https://github.com/octoprobe/testbed_tutorial.git
    cd testbed_tutorial/

## python

.. code::

    echo 'source ~/venv_octoprobe/bin/activate' >> ~/.profile
    python -m venv ~/venv_octoprobe

    source ~/venv_octoprobe/bin/activate
    pip install --upgrade -r requirements.txt -r requirements_dev.txt

## Software requiring root access

Will be used by mpremote and others

.. code::

    sudo usermod -a -G dialout $USER


APT

.. code::

    sudo usermod -a -G dialout $USER

    op install

Now `op install` will instruct you to:

.. code::

    sudo chown root:root ~/octoprobe_downloads/binaries/aarch64/*
    sudo chmod a+s ~/octoprobe_downloads/binaries/aarch64/*
    sudo cp -p ~/octoprobe_downloads/binaries/aarch64/* /usr/sbin
