from homeassistant.helpers import config_validation as cv
import voluptuous as vol
import logging
from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config, HomeAssistant

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
    if config.get(DOMAIN) is None:
        # We get her if the integration is set up using config flow
        return True

    try:
        await hass.config_entries.async_forward_entry(config, "sensor")
        _LOGGER.info("Successfully added sensor from the avfallsor integration")
    except ValueError:
        pass

    hass.async_create_task(
        hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_IMPORT}, data={}
        )
    )
    return True

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up woocommerce_stats as config entry."""
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(config_entry, "sensor")
    )
    return True


async def async_remove_entry(hass, config_entry):
    try:
        await hass.config_entries.async_forward_entry_unload(config_entry, "sensor")
        _LOGGER.info("Successfully removed sensor from the woocommerce_stats integration")
    except ValueError:
        pass