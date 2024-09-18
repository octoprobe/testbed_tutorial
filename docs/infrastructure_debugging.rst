

Use case: Interrupt a test and dubug the MCU on REPL

* Step 1: Leave test
  * Add to your testcode: `mcu.dut.inspection_exit()`
  * This will exit the test without resetting anything. The port number is printed to the console.
* Step 2: Verify white relays LEDS
* Step 3: Connect MCU using Thonny

What happens
* When starting the test, ALL tentacles - including the ones which are NOT configured - will be power cycled.
* Now, the tentacles which are referenced in the parameter list of the test will be initialized:
  * The DUT MCU will be powercycled.
  * The relais are set according to `testbed_tentacles.py / relays_closed`.