#from homeassistant.const import TEMP_CELSIUS
import logging
import serial
from homeassistant.helpers.entity import Entity
from homeassistant.const import (
    CONF_NAME, CONF_UNIT_OF_MEASUREMENT, CONF_PORT)
from homeassistant.components.sensor import PLATFORM_SCHEMA
import voluptuous as vol
import homeassistant.helpers.config_validation as cv


# turn on the LEDs
# ser.write("L,1\r")
# ser.write("C,0\r")

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
        self.ser = serial.Serial(port, 9600)
        _LOGGER.info("Serial for Atlas @%s = %s  " % (port,self.ser))
        self._state = None
        self._name = name
        ezos = {"ph": ['ph', 'pH', 'mdi:alpha-h-circle'],
               "orp": ['orp', 'mV', 'mdi:alpha-r-circle'],
               "d.o.": ['dissolved_oxygen','mV', 'mdi:alpha-x-circle'],
               "ec": ['conductivity', "EC", 'mdi:alpha-c-circle']}
        ezo = self._read("I").lower().split(',')
        if len(ezo)>2 and ezo[1] in ezos:
            self._ezo_dev = ezos[ezo[1]][0]
            self._ezo_uom = ezos[ezo[1]][1]
            self._ezo_icon = ezos[ezo[1]][2]
            _LOGGER.info("Atlas %s detected " % self._ezo_dev)
            self._name += ("_" + self._ezo_dev) 

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
            if line[0]=="*" and line[-1]=="\r": break
            if terminator in line: return line.replace(terminator,"")

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
