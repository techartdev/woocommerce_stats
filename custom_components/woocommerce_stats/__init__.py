from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant import config_entries
import logging

_LOGGER = logging.getLogger(__name__)

DOMAIN = "woocommerce_stats"


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up WooCommerce Stats integration using YAML (deprecated in modern HA)."""
    if config.get(DOMAIN) is None:
        # We get her if the integration is set up using config flow
        return True

    try:
        await hass.config_entries.async_forward_entry_setup(config, "sensor")
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
    """Set up WooCommerce Stats from a config entry."""
    _LOGGER.debug("async_setup_entry called for WooCommerce Stats.")

    # Forward the entry setup to the sensor platform
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(config_entry, "sensor")
    )
    _LOGGER.debug("Forwarded config entry to the sensor platform.")
    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload WooCommerce Stats config entry."""
    _LOGGER.debug("async_unload_entry called for WooCommerce Stats.")

    # Forward the unloading to the sensor platform
    unload_ok = await hass.config_entries.async_forward_entry_unload(config_entry, "sensor")
    if unload_ok:
        _LOGGER.debug("Successfully unloaded WooCommerce Stats sensors.")
    else:
        _LOGGER.error("Failed to unload WooCommerce Stats sensors.")

    return unload_ok
