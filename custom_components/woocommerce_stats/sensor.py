from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from woocommerce import API
import logging

_LOGGER = logging.getLogger(__name__)

# Constants
DOMAIN = "woocommerce_stats"

# WooCommerce API Wrapper
def get_woocommerce_api(url, consumer_key, consumer_secret):
    return API(
        url=url,
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        version="wc/v3"
    )

# Sensor Entity
class WooCommerceSensor(SensorEntity):
    def __init__(self, coordinator, name, key):
        self.coordinator = coordinator
        self._name = name
        self._key = key

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self.coordinator.data.get(self._key)

    async def async_update(self):
        await self.coordinator.async_request_refresh()

# Setup Platform
async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    url = config["url"]
    consumer_key = config["consumer_key"]
    consumer_secret = config["consumer_secret"]

    wc_api = get_woocommerce_api(url, consumer_key, consumer_secret)

    async def fetch_data():
        try:
            return wc_api.get("reports/totals").json()
        except Exception as e:
            _LOGGER.error("Error fetching data from WooCommerce: %s", e)
            raise UpdateFailed(e)

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="woocommerce_stats",
        update_method=fetch_data,
        update_interval=timedelta(minutes=10),
    )

    await coordinator.async_refresh()

    sensors = [
        WooCommerceSensor(coordinator, "Total Sales", "sales"),
        WooCommerceSensor(coordinator, "Total Orders", "orders"),
    ]
    async_add_entities(sensors)
