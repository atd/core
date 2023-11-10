"""The ovos integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import discovery

from .const import DOMAIN
from .entity import Entity

_LOGGER = logging.getLogger(__name__)

ENTRY_PLATFORMS: list[Platform] = [Platform.NUMBER]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up ovos from a config entry."""

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN].setdefault("entries", {})

    hass.data[DOMAIN]["entries"][entry.entry_id] = Entity(entry)

    await hass.config_entries.async_forward_entry_setups(entry, ENTRY_PLATFORMS)
    discovery.load_platform(hass, Platform.NOTIFY, DOMAIN, {}, {})

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(
        entry, ENTRY_PLATFORMS
    ):
        entry_id = entry.entry_id

        hass.data[DOMAIN]["entries"][entry_id].unload()
        hass.data[DOMAIN]["entries"].pop(entry_id)

    return unload_ok
