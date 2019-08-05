"""Atlas Scientific"""
import logging

# The domain of your component. Should be equal to the name of your component.
DOMAIN = "atlas_scientific"
_LOGGER = logging.getLogger(__name__)

def setup(hass, config):
    """Setup the service example component."""
    def compensate_temperature(call):
        """My first service."""
        _LOGGER.info('Compensate temperature to ...', call.data)
        # _LOGGER.info('Compensate temperature to ...', call.data.get('temperature'))

    # Register our service with Home Assistant.
    hass.services.register(DOMAIN, 'compensate_temp',  compensate_temperature)

    # Return boolean to indicate that initialization was successfully.
    return True
