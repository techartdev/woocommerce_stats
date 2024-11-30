from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant import config_entries
import logging

_LOGGER = logging.getLogger(__name__)

DOMAIN = "woocommerce_stats"
PLATFORMS = ["sensor"]


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the WooCommerce Stats integration."""
    # Handle YAML configuration (if any, but not recommended with config entries).
    _LOGGER.debug("async_setup called for WooCommerce Stats.")
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up WooCommerce Stats from a config entry."""
    _LOGGER.debug("async_setup_entry called for WooCommerce Stats.")

    # Store config entry data
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # Forward the config entry to the sensor platform
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    _LOGGER.debug("Config entry forwarded to platforms: %s", PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.debug("async_unload_entry called for WooCommerce Stats.")

    # Unload platforms
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    # Cleanup data if platforms are unloaded successfully
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
        _LOGGER.debug("Successfully unloaded WooCommerce Stats.")

    return unload_ok


async def async_remove_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle removal of a config entry."""
    _LOGGER.debug("async_remove_entry called for WooCommerce Stats.")
    # Perform any additional cleanup or resource deallocation here