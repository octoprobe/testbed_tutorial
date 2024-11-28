Tentacle `MCU_LOLIN_C3_MINI`
============================

Supported FUTs: FUT_EXTMOD_HARDWARE

v0.1 FUT_EXTMOD_HARDWARE

:download:`Schematics </../schematics_kicad/schematics.pdf>`

.. image:: top_view.jpg
   :height: 500px
   :align: center

* `Pinout LOLIN_C3_MINI <https://www.wemos.cc/en/latest/_static/boards/c3_mini_v2.1.0_4_16x9.png>`_
* `Datasheet ESP32-C3FH4 <https://www.espressif.com/sites/default/files/documentation/esp32-c3_datasheet_en.pdf>`_

Pins assignements
-----------------

BOOTSEL is NOT required

====  =======  ========  =================[[]]
CPU   Pin      signals   rationale
====  =======  ========  ===================
\     GND                GND
\     21       TX        FUT_EXTMOD_HARDWARE
\     20       RX        FUT_EXTMOD_HARDWARE
====  =======  ========  ===================
