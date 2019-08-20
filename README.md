# raspipool
Swimming-Pool Automation Systen with Raspberry Pi + Home Assistant

Goal:

Build a cost-effective, easy-to-install, easy-to-use "Swimming-Pool Automation System" with basic functions for most of small-medium size pools.

- Filter control (fixed and dual-speed pump)
- 3 sensors:
  - temp (one-wire DS18B20)
  - [ph](https://www.atlas-scientific.com/product_pages/circuits/ezo_ph.html) and [orp](https://www.atlas-scientific.com/product_pages/circuits/ezo_orp.html) with [EZO circuits](https://www.atlas-scientific.com/product_pages/components/ezo-carrier-board.html). A custom UART sensor for HA has been developed.
- and minimun of 4 controllers (relays):
  - pump on/off
  - pump speed (high/low)
  - muriatic injection (to reduce pH)
  - bleach injection
 
 System is intended to automagically control basic functions and notification all possible events.
 
 TODO:
 - External sensor to measure power consumption and [safe motor](https://en.wikipedia.org/wiki/Magnetic_starter) (probably based on sonoff POW)
 - Integrate mega-io board (relays and ACD)
 - SWC – Salt Water Chlorinator 
