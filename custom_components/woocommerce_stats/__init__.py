import logging
from datetime import timedelta

import async_timeout
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.storage import Store

from woocommerce import API
from .const import DOMAIN, PLATFORMS, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)
STORAGE_VERSION = 1

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up WooCommerce Stats from a config entry."""
    config = entry.data
    options = entry.options

    # Persistent storage for tokens or data
    store = Store(hass, STORAGE_VERSION, f"woocommerce_{entry.entry_id}")

    # Initialize WooCommerce API
    wc_api = API(
        url=config["url"],
        consumer_key=config["consumer_key"],
        consumer_secret=config["consumer_secret"],
        version="wc/v3"
    )

    async def async_update_data():
        """Fetch data from WooCommerce API."""
        async with async_timeout.timeout(30):
            try:
                # Fetch data from the WooCommerce API
                response = wc_api.get("reports/sales").json()
                _LOGGER.debug("WooCommerce API response: %s", response)
                await store.async_save(response)  # Save response to persistent storage
                return response
            except Exception as e:
                _LOGGER.error("Error fetching data from WooCommerce: %s", e)
                raise UpdateFailed(f"Error communicating with WooCommerce: {e}")

    # Data update coordinator for periodic fetching
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="WooCommerce Stats",
        update_method=async_update_data,
        update_interval=timedelta(seconds=options.get("data_interval", DEFAULT_SCAN_INTERVAL)),
    )

    # Perform initial data fetch
    await coordinator.async_config_entry_first_refresh()

    # Store the coordinator in the Home Assistant data object
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "coordinator": coordinator,
        "api": wc_api,
        "store": store,
    }

    # Forward the entry to supported platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a WooCommerce Stats config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok