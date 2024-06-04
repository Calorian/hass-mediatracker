"""My Custom Component init file."""
import logging
import voluptuous as vol

from homeassistant.core import HomeAssistant
from homeassistant.helpers import discovery
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

DOMAIN = "media_tracker"

CONF_NAME = "name"
CONF_SSL = "ssl"
CONF_HOST = "host"
CONF_PORT = "port"
CONF_TOKEN = "token"
CONF_DAYS = "days"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_TOKEN): cv.string,
                vol.Optional(CONF_NAME, default='MediaTracker Upcoming'): cv.string,
                vol.Optional(CONF_SSL, default=False): cv.boolean,
                vol.Optional(CONF_HOST, default='localhost'): cv.string,
                vol.Optional(CONF_PORT, default=7481): cv.port,
                vol.Optional(CONF_DAYS, default=7): cv.positive_int,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the custom component."""
    conf = config[DOMAIN]
    hass.data[DOMAIN] = conf

    _LOGGER.info("Setting up my custom component with configuration: %s", conf)

    # Load platforms (e.g., sensor)
    hass.async_create_task(
        discovery.async_load_platform(hass, "sensor", DOMAIN, {}, config)
    )

    return True
