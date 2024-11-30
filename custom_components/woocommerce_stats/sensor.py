from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from datetime import timedelta
from woocommerce import API
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
import logging
from homeassistant.components.sensor import PLATFORM_SCHEMA

_LOGGER = logging.getLogger(__name__)

DOMAIN = "woocommerce_stats"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional("url", default=""): cv.string,
        vol.Optional("consumer_key", default=""): cv.string,
        vol.Optional("consumer_secret", default=""): cv.string,
    }
)


MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=10)


class WooCommerceData:
    """Class to manage fetching data from WooCommerce API."""

    def __init__(self, url, consumer_key, consumer_secret):
        self.api = API(
            url=url,
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            version="wc/v3"
        )
        self.data = {}

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self):
        """Fetch data from WooCommerce API."""
        _LOGGER.debug("Fetching data from WooCommerce API...")
        try:
            response = await self.api.get_async("reports/totals")
            self.data = response.json()
            _LOGGER.debug("WooCommerce data fetched: %s", self.data)
        except Exception as e:
            _LOGGER.error("Error fetching data from WooCommerce: %s", e)
            self.data = {}


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up WooCommerce sensors."""
    url = config_entry.data["url"]
    consumer_key = config_entry.data["consumer_key"]
    consumer_secret = config_entry.data["consumer_secret"]

    wc_data = WooCommerceData(url, consumer_key, consumer_secret)
    await wc_data.async_update()

    async_add_entities([
        WooCommerceSensor(wc_data, "Total Sales", "total_sales"),
        WooCommerceSensor(wc_data, "Total Orders", "total_orders"),
    ])


class WooCommerceSensor(SensorEntity):
    """Representation of a WooCommerce sensor."""

    def __init__(self, data, name, key):
        self.data = data
        self._name = name
        self._key = key

    async def async_update(self):
        """Fetch the latest data from WooCommerce."""
        await self.data.async_update()

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the current state of the sensor."""
        return self.data.data.get(self._key, 0)

    @property
    def extra_state_attributes(self):
        """Return additional attributes."""
        return {"last_update": self.data.data}

    @property
    def unique_id(self):
        """Return a unique ID for this sensor."""
        return f"woocommerce_stats_{self._key}"