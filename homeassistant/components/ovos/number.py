"""Manage OVOS number entities."""
import logging

from ovos_bus_client import Message

from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import Entity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the OVOS number platform."""

    entity = hass.data[DOMAIN]["entries"][entry.entry_id]
    async_add_entities([Volume(entity)])


class Volume(NumberEntity):
    """Representation of OVOS device volume."""

    _attr_native_min_value = 0
    _attr_native_max_value = 1

    def __init__(self, entity: Entity) -> None:
        """Initialize the Ovos Volume Number entity."""
        self._entity = entity
        self._attr_unique_id = f"{entity.name}_volume"
        self._attr_name = f"{entity.name} Volume"
        self._attr_device_info = entity.device_info

        self._entity.on_volume_get_response(self._on_volume_get_response)

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        self._entity.set_volume(value)

        self.async_write_ha_state()

    def _on_volume_get_response(self, message: Message) -> None:
        self._attr_native_value = message.data["percent"]

        self.async_write_ha_state()
