from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, COORDINATOR, SENSORS, ATTRIBUTION

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up WooCommerce Stats sensors from a config entry."""
    data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = data[COORDINATOR]

    entities = []
    for description in SENSORS:
        entities.append(
            WooCommerceStatsEntity(
                description=description,
                coordinator=coordinator,
                config_entry=config_entry,
            )
        )

    async_add_entities(entities)


class WooCommerceStatsEntity(CoordinatorEntity, SensorEntity):
    """Representation of a WooCommerce Stats sensor."""

    def __init__(self, description, coordinator, config_entry):
        """Initialize the WooCommerce Stats sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._config_entry = config_entry
        self._attr_unique_id = f"{DOMAIN}_{description.key}_{config_entry.entry_id}"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get(self.entity_description.key)

    @property
    def extra_state_attributes(self):
        """Return extra attributes for the sensor."""
        return {
            ATTR_ATTRIBUTION: ATTRIBUTION,
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
