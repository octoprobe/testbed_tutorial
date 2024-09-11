.. Octoprobe: testbed_tutorial documentation master file, created by
   sphinx-quickstart on Tue Sep 10 15:55:53 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Octoprobe: testbed_tutorial documentation
=========================================

Add your content using `reStructuredText` syntax. See the
`reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_
documentation for details.

.. automodule:: tests
    :members:

.. code::

    .. toctree::
        :maxdepth: 2
        :caption: Contents:
        :includehidden:

        license.rst
        README_installation_ubuntu.rst
        README_installation_raspberry.rst
        README.rst
        tentacle_DAQ_saleae/README.rst
        tentacle_DEVICE_potpourri/README.rst
        tentacle_MCU_PYBV11/README.rst
        tentacle_MCU_RPI_PICO/README.rst

.. toctree::
    :glob:
    :maxdepth: 2
    :caption: Contents:
    :includehidden:

    *
    */*

Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
