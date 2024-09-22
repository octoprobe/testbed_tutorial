Signals
=======

`Octobus` is the 40pin ribbon wire cable which connects the tentacles.

===========  =================  =========  ==========  =============  ===============================
Octobus Pin  signal             `FUT_I2C`  `FUT_UART`  `FUT_ONEWIRE`  Comment                        
===========  =================  =========  ==========  =============  ===============================
5            `SIGNAL_TRIGGER1`  trigger    trigger     trigger        logic analyzer, measures delays
7            GND              
9            `SIGNAL_TRIGGER2`  trigger    trigger     trigger        logic analyzer, measures delays
11           GND              
13           `SIGNAL_DATA1`     SCL        TX          data         
15           GND              
17           `SIGNAL_DATA2`     SDA        RX          \            
19           GND              
===========  =================  =========  ==========  =============  ===============================

All signals are 3.3V.

Why are the `SIGNAL_DATA1/2` lines shared for different protocols? The current tentacles only provide limited relays, so only a few data lines may be controlled.
