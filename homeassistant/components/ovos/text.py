"""Manage OVOS text entities."""
import logging

from ovos_bus_client import Message

from homeassistant.components.text import TextEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import Entity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the OVOS text platform."""

    entity = hass.data[DOMAIN]["entries"][entry.entry_id]
    async_add_entities([Utterance(entity)])


class Utterance(TextEntity):
    """Representation of OVOS utterance."""

    def __init__(self, entity: Entity) -> None:
        """Initialize the Ovos Utterance entity."""
        self._entity = entity
        self._attr_unique_id = f"{entity.name}_utterance"
        self._attr_name = f"{entity.name} Utterance"
        self._attr_device_info = entity.device_info
        self._attr_native_value = ""

        self._entity.on("recognizer_loop:utterance", self._on_get_response)

    async def async_set_value(self, value: str) -> None:
        """Update the current value."""
        self._entity.emit("recognizer_loop:utterance", {"utterances": [value]})

        self.async_write_ha_state()

    def _on_get_response(self, message: Message) -> None:
        self._attr_native_value = message.data["utterances"][0]

        self.async_write_ha_state()
