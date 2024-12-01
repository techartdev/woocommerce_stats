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
        sales_url = f"{config['url']}/wp-json/wc/v3/reports/sales"
        orders_url = f"{config['url']}/wp-json/wc/v3/reports/orders/totals"
        auth = aiohttp.BasicAuth(config["consumer_key"], config["consumer_secret"])

        async with async_timeout.timeout(30):
            try:
                async with session.get(sales_url, auth=auth) as sales_response:
                    if sales_response.status != 200:
                        raise UpdateFailed(f"Failed to fetch sales data. HTTP Status: {sales_response.status}")
                    sales_data = await sales_response.json(content_type=None)
                    if not isinstance(sales_data, list) or not sales_data:
                        raise UpdateFailed("Unexpected sales data format from WooCommerce API.")
                    sales_data = sales_data[0]  # Extract the first element

                async with session.get(orders_url, auth=auth) as orders_response:
                    if orders_response.status != 200:
                        raise UpdateFailed(f"Failed to fetch orders data. HTTP Status: {orders_response.status}")
                    orders_data = await orders_response.json(content_type=None)
                    if not isinstance(orders_data, list):
                        raise UpdateFailed("Unexpected orders data format from WooCommerce API.")

                # Combine data from both reports
                combined_data = {
                    "sales": sales_data,
                    "orders": {item["slug"]: item["total"] for item in orders_data},
                }
                _LOGGER.debug("Combined WooCommerce API response: %s", combined_data)

                # Save combined data to persistent storage
                await store.async_save(combined_data)

                return combined_data
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