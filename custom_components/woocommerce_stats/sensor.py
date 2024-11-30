from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, COORDINATOR, SENSORS, ATTRIBUTION

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up WooCommerce Stats sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id][COORDINATOR]

    # Create sensor entities based on the SENSORS definition
    async_add_entities([
        WooCommerceStatsEntity(coordinator, sensor_description, entry)
        for sensor_description in SENSORS
    ])

class WooCommerceStatsEntity(CoordinatorEntity, SensorEntity):
    """Representation of a WooCommerce Stats sensor."""

    def __init__(self, coordinator, description: dict, config_entry: ConfigEntry):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_name = description["name"]
        self._attr_icon = description.get("icon")
        self._attr_native_unit_of_measurement = description.get("unit")
        self._attr_unique_id = f"{DOMAIN}_{description['key']}_{config_entry.entry_id}"
        self._description_key = description["key"]

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get(self._description_key)

    @property
    def extra_state_attributes(self):
        """Return additional attributes for the sensor."""
        return {
            "attribution": ATTRIBUTION,
            "last_updated": self.coordinator.last_update_success,
        }

    @property
    def device_info(self):
        """Return device info for the sensor."""
        return {
            "identifiers": {(DOMAIN, self._config_entry.entry_id)},
            "name": "WooCommerce Stats",
            "manufacturer": "WooCommerce",
            "model": "API Integration",
        }
