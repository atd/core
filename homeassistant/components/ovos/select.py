"""Manage OVOS select entities."""
import logging

from ovos_bus_client import Message

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import Entity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the OVOS select platform."""

    entity = hass.data[DOMAIN]["entries"][entry.entry_id]
    async_add_entities([GuiPage(entity)])


PAGES = ["night_time", "main", "boxes"]


class GuiPage(SelectEntity):
    """Representation of OVOS Main View Page."""

    def __init__(self, entity: Entity) -> None:
        """Initialize the Ovos GuiPage select entity."""
        self._entity = entity
        self._attr_unique_id = f"{entity.name}_gui_page"
        self._attr_name = f"{entity.name} GUI Page"
        self._attr_device_info = entity.device_info
        self._attr_current_option = None
        self._attr_options = PAGES
        self._attr_translation_key = "main_view_page"

        self._entity.on(
            "ovos.gui.main_view.current_index.get.response", self._on_get_response
        )
        self._entity.emit("ovos.gui.main_view.current_index.get")

    async def async_select_option(self, option: str) -> None:
        """Update the current value."""
        self._entity.emit(
            "ovos.gui.main_view.current_index.set",
            {"current_index": PAGES.index(option)},
        )

        self.async_write_ha_state()

    def _on_get_response(self, message: Message) -> None:
        self._attr_current_option = PAGES[message.data["current_index"]]

        self.async_write_ha_state()
