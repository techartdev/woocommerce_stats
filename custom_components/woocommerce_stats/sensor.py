from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from datetime import timedelta
from woocommerce import API
import logging

_LOGGER = logging.getLogger(__name__)

DOMAIN = "woocommerce_stats"

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities):
    """Set up WooCommerce Stats sensors via a config entry."""
    # Get API details from the config entry
    url = config_entry.data["url"]
    consumer_key = config_entry.data["consumer_key"]
    consumer_secret = config_entry.data["consumer_secret"]

    # Initialize WooCommerce API
    wc_api = API(
        url=url,
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        version="wc/v3"
    )

    # Data Update Coordinator for fetching data
    async def fetch_data():
        try:
            _LOGGER.debug("Fetching data from WooCommerce API...")
            response = wc_api.get("reports/totals").json()
            return {
                "total_sales": response.get("sales", 0),
                "total_orders": response.get("orders", 0),
                "total_customers": response.get("customers", 0),
            }
        except Exception as err:
            _LOGGER.error("Error fetching data from WooCommerce: %s", err)
            raise UpdateFailed(err)

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="woocommerce_stats",
        update_method=fetch_data,
        update_interval=timedelta(minutes=10),
    )

    # Refresh coordinator data
    await coordinator.async_refresh()

    # Create sensor entities
    async_add_entities([
        WooCommerceSensor(coordinator, "Total Sales", "total_sales"),
        WooCommerceSensor(coordinator, "Total Orders", "total_orders"),
        WooCommerceSensor(coordinator, "Total Customers", "total_customers"),
    ])

class WooCommerceSensor(SensorEntity):
    """Representation of a WooCommerce sensor."""

    def __init__(self, coordinator, name, key):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._name = name
        self._key = key

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get(self._key)

    @property
    def should_poll(self):
        """No polling needed, coordinator handles updates."""
        return False

    @property
    def available(self):
        """Return True if data is available."""
        return self.coordinator.last_update_success

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            "data_fetched": self.coordinator.data
        }

    async def async_update(self):
        """Manually trigger an update."""
        await self.coordinator.async_request_refresh()

    async def async_added_to_hass(self):
        """Subscribe to coordinator updates."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )
