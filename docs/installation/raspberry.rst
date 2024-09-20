Installation Raspberry Pi 4
===========================

Prepare SD Card
---------------

* rpi-imager

  | Raspberry Pi OS Lite (64-bit)  
  | 2024-07-04, 0.4GBytes

* OS customisation

  * hostname: octoprobe
  * | User/pw: octoprobe/octoprobe
    | Services, enable ssh: yes

First boot
----------

:code:`ssh octoprobe@raspberrypi.local octoprobe/octoprobe`


Now follow :doc:`/installation/ubuntu`.

Upgrade python 3.11.2 → 3.12.6
-------------------------------

.. code::

  wget https://www.python.org/ftp/python/3.12.6/Python-3.12.6.tgz

  sudo apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev  libsqlite3-dev

  tar -xf Python-3.12.6.tgz 
  cd Python-3.12.6/

  ./configure --enable-optimizations
  sudo make altinstall

  sudo rm /usr/bin/python
  sudo ln -s /usr/local/bin/python3.12 /usr/bin/python
