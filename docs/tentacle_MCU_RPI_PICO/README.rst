Tentacle `MCU_RPI_PICO`/`MCU_RPI_PICO2`
===========================================

The same tentacle may be applied for the

| Board | Tentacle name | Variants |
| - | - | - |
| Pico rp2040 | MCU_RPI_PICO | arm |
| Pico rp2340 | MCU_RPI_PICO2 | arm and risc-V

.. image:: top_view.jpg

.. image:: https://www.raspberrypi.com/documentation/microcontrollers/images/pico-pinout.svg)


## Pins used

| CPU | Pin | signals | rationale |
| - | - | - | - |
| - | BOOTSEL | | |
| GP20 | 26 | trigger1 |  |
| GP21 | 27 | trigger2 |  |
| GP16 | 21 | TX | UART0 |
| GP17 | 22 | RX | UART0 |
| GP19 | 25 | SCL | I2C1 |
| GP18 | 24 | SDA | I2C1 |
| GP14 | 19 | onewire |  |
