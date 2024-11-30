import logging
from datetime import timedelta

import async_timeout
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.storage import Store

import aiohttp
from .const import DOMAIN, PLATFORMS, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)
STORAGE_VERSION = 1

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up WooCommerce Stats from a config entry."""
    config = entry.data
    options = entry.options

    # Persistent storage for tokens or data
    store = Store(hass, STORAGE_VERSION, f"woocommerce_{entry.entry_id}")

    # Asynchronous HTTP client session
    session = aiohttp.ClientSession()

    async def async_update_data():
        """Fetch data from WooCommerce API."""
        url = f"{config['url']}/wp-json/wc/v3/reports/sales"
        auth = aiohttp.BasicAuth(config["consumer_key"], config["consumer_secret"])

        async with async_timeout.timeout(30):
            try:
                async with session.get(url, auth=auth) as response:
                    if response.status == 401:
                        _LOGGER.error("Invalid WooCommerce API credentials.")
                        raise UpdateFailed("Invalid API credentials.")
                    if response.status != 200:
                        _LOGGER.error(
                            "Failed to fetch data from WooCommerce API. HTTP Status: %s",
                            response.status,
                        )
                        raise UpdateFailed(f"Failed to fetch data. HTTP Status: {response.status}")
                    
                    # Parse JSON response
                    result = await response.json()
                    _LOGGER.debug("WooCommerce API response: %s", result)
                    
                    # Save to persistent storage
                    await store.async_save(result)
                    
                    return result
            except aiohttp.ClientError as e:
                _LOGGER.error("Error communicating with WooCommerce API: %s", e)
                raise UpdateFailed(f"Error communicating with WooCommerce API: {e}") from e

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
        "session": session,  # Store aiohttp session for cleanup
        "store": store,
    }

    # Forward the entry to supported platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a WooCommerce Stats config entry."""
    # Retrieve stored session
    session = hass.data[DOMAIN][entry.entry_id]["session"]

    # Unload platforms
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        # Close the aiohttp session
        await session.close()

        # Clean up stored data
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok