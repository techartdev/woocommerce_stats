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
    _LOGGER.debug("async_setup_entry called for WooCommerce Stats.")

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(config_entry, "sensor")
    )
    return True

async def async_unload_entry(hass, config_entry):
    """Unload a config entry."""
    _LOGGER.debug("async_unload_entry called for WooCommerce Stats.")
    await hass.config_entries.async_forward_entry_unload(config_entry, "sensor")
    return True