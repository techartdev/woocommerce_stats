from homeassistant.helpers import config_validation as cv
import voluptuous as vol
import logging

_LOGGER = logging.getLogger(__name__)

DOMAIN = "woocommerce_stats"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required("url"): cv.url,
                vol.Required("consumer_key"): cv.string,
                vol.Required("consumer_secret"): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

async def async_setup(hass, config):
    """Set up WooCommerce Stats integration."""
    return True

async def async_setup_entry(hass, config_entry):
    """Set up WooCommerce Stats from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][config_entry.entry_id] = {
        "url": config_entry.data["url"],
        "consumer_key": config_entry.data["consumer_key"],
        "consumer_secret": config_entry.data["consumer_secret"],
    }

    _LOGGER.info("WooCommerce Stats integration has been set up via config entry.")
    return True

async def async_unload_entry(hass, config_entry):
    """Unload a config entry."""
    hass.data[DOMAIN].pop(config_entry.entry_id)
    return True
