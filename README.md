# raspool
Pool Automation Systen with Raspberry Pi + Home Assistant
Goal:
Build a cost-effective easy-to-install easy-to-use automation system with basic functions for most of little-medium pools.

- Filter control (fixed and dual-speed pump)
- 3 sensors:
  - temp (one-wire DS18B20)
  - ph and orp with EZO circuits (a custom sensor for HA has been developed).
- and minimun of 4 controllers (relays):
  - pump on/off
  - pump speed (high/low)
  - muriatic injection (to reduce pH)
  - bleach injection / SWC – Salt Water Chlorinator
 
 TODO:
 - External sensor to measure power consumption (probably based on sonoff POW)
 - Integrate mega-io board (relays and ACD)
