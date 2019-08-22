# raspipool
Swimming-Pool Automation Systen with Raspberry Pi + Home Assistant

## Goal:

Build a cost-effective, easy-to-install, easy-to-use "Swimming-Pool Automation System" with basic functions for most of small-medium size pools.

- Filter control (fixed and dual-speed pump)
- 3 sensors:
  - temp (one-wire DS18B20)
  - [ph](https://www.atlas-scientific.com/product_pages/circuits/ezo_ph.html) and [orp](https://www.atlas-scientific.com/product_pages/circuits/ezo_orp.html) with [EZO circuits](https://www.atlas-scientific.com/product_pages/components/ezo-carrier-board.html). A custom UART sensor for HA has been developed.
- and minimun of [4 relays](https://aliexpress.com/item/32961638909.html) [or 6](https://aliexpress.com/item/32997012084.html) controlling :
  - pump on/off and pump speed (high/low)
  - muriatic injection (to reduce pH) and bleach injection
 
 System is intended to automagically control basic functions and notification all possible events.
 
 ## Install
 0. Install raspbian and Home Assistant ([prefered method](https://www.home-assistant.io/docs/installation/raspberry-pi/) as I use it now) (or HASS.IO)
 1. Just copy 'custom_components', 'packages' folders (with all paths and contents) and 'ui-lovelace.yaml' frontend file in homeassistant conf_dir ( i.e. /home/homeassistant/.homeassistant/ ).
 2. Modify your 'configuration.yaml' (including '  packages: !include_dir_named packages', disabling automations and discovery and lovelace in yaml mode) as example in code
 3. Create/modify proper 'secrets.yaml' for apis (latitude/longitude, pushbullet api, openweathermap api, etc).
 
 
 ## TODO:
 - External sensor to measure power consumption and [safe motor](https://en.wikipedia.org/wiki/Magnetic_starter) (probably based on sonoff POW)
 - Integrate mega-io board (relays and ACD with )
 - SWC – Salt Water Chlorinator 
