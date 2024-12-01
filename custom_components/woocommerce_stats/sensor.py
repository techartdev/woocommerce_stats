from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.sensor import SensorEntityDescription

from .const import DOMAIN, COORDINATOR, SENSORS, ATTRIBUTION

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up WooCommerce Stats sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id][COORDINATOR]

    # Create sensor entities based on the SENSORS definition
    async_add_entities([
        WooCommerceStatsEntity(coordinator, sensor_description, entry)
        for sensor_description in SENSORS
    ])

class WooCommerceStatsEntity(CoordinatorEntity, SensorEntity):
    """Representation of a WooCommerce Stats sensor."""

    def __init__(self, coordinator, description: SensorEntityDescription, config_entry: ConfigEntry):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._config_entry = config_entry
        self._attr_unique_id = f"{DOMAIN}_{description.key}_{config_entry.entry_id}"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        key = self.entity_description.key
        if key.startswith("orders_"):
            # Fetch order totals by slug
            slug = key.replace("orders_", "")
            return self.coordinator.data["orders"].get(slug)
        return self.coordinator.data["sales"].get(key)

    @property
    def extra_state_attributes(self):
        """Return additional attributes for the sensor."""
        return {
            "attribution": ATTRIBUTION,
            "last_updated": self.coordinator.last_update_success,
        }

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._config_entry.entry_id)},
            "name": "WooCommerce Stats",
            "manufacturer": "WooCommerce",
            "model": "WooCommerce API",
        }
