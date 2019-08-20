# Under MIT licence
# Release 0.1 (06/08/2019) by segalion at gmail
# ORP & pH tested. DO & EC from datasheets, so possible errors like ORP/OR


import logging
import serial
from homeassistant.helpers.entity import Entity
from homeassistant.const import (
    CONF_NAME, CONF_UNIT_OF_MEASUREMENT, CONF_PORT)
from homeassistant.components.sensor import PLATFORM_SCHEMA
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
#from homeassistant.const import TEMP_CELSIUS

_LOGGER = logging.getLogger(__name__)

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_PORT): cv.string,
    vol.Optional(CONF_NAME, default='ezo'): cv.string
})

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""
    port=config.get(CONF_PORT)
    name=config.get(CONF_NAME)
    #add_entities([[AtlasSensor(
    #    name=config.get(CONF_NAME),
    #    port=config.get(CONF_PORT)
    #)])
    add_devices([AtlasSensor(name,port)])

class AtlasSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, name, port):
        """Initialize the sensor."""
        self.ser = serial.Serial(port, 9600, timeout=3, write_timeout=3)
        _LOGGER.info("Serial for Atlas EZO @%s = %s" % (port,self.ser))
        self._state = None
        self._name = name
        ezos = {"ph": ['ph', 'pH', 'mdi:alpha-h-circle'],
               "orp": ['orp', 'mV', 'mdi:alpha-r-circle'],
               "or": ['orp', 'mV', 'mdi:alpha-r-circle'],
               "do": ['dissolved_oxygen','mV', 'mdi:alpha-x-circle'],
               "d.o.": ['dissolved_oxygen','mV', 'mdi:alpha-x-circle'],
               "ec": ['conductivity', "EC", 'mdi:alpha-c-circle']}
        # Reset buffer
        self._read("")
        # Get Status
        status = self._read("Status")
        # Set response ON
        ok = self._read("*OK,1")
        ok += self._read("RESPONSE,1")
        # Set continuos  mode OFF
        c = self._read("C,0")
        # Get kind of EZO
        for i in range(5):
            ezo = self._read("I")
            if ezo is not None:
                ezo = ezo.lower().split(',')
                if len(ezo)>2 and ezo[1] in ezos:
                    self._ezo_dev = ezos[ezo[1]][0]
                    self._ezo_uom = ezos[ezo[1]][1]
                    self._ezo_icon = ezos[ezo[1]][2]
                    self._name += ("_" + self._ezo_dev)
                    break
        _LOGGER.info("Atlas EZO '%s' detected [Status=%s, Ok=%s, c=%s]", ezo,status,ok,c)

    @property
    def name(self):
        """Return the name of the sensor."""
        # return "Atlas Scientific"
        return self._name

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return self._ezo_dev

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return self._ezo_icon

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._ezo_uom

    def _read(self,command="R",terminator="\r*OK\r"):
        self.ser.write((command + "\r").encode())
        line = ""
        for i in range(50):
            line += self.ser.read().decode()
            if ( line[0]=="*" and line[-1]=="\r") or terminator in line: break
        return line.replace(terminator,"")

    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self._read()
        _LOGGER.debug("update state = '%s'" % self._state)
        return

        self.ser.write("R\r".encode())
        line = ""
        while True:
            data = self.ser.read().decode()
            if(data == "\r"):
                break
            else:
                line = line + data
        try:
            self._state = float(line)
        except:
            _LOGGER.info("readed '%s'" % line)

    def __del__(self):
        """close the sensor."""
        self.ser.close()
