"""OVOS Entry wrapper."""
from collections.abc import Callable
import logging
from typing import Any

from ovos_bus_client import Message, MessageBusClient

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class Entity:
    """Wrapper of an OVOS entry."""

    def __init__(self, config: ConfigEntry) -> None:
        """Initialize entry and setups connection."""
        self.config = config

        self.client = MessageBusClient(
            host=self.config.data["host"], port=self.config.data["port"]
        )
        self.client.run_in_thread()

    @property
    def name(self) -> str:
        """Name of the OVOS entry."""
        return self.config.data["host"]

    @property
    def device_info(self) -> DeviceInfo:
        """OVOS entry device."""
        return DeviceInfo(identifiers={(DOMAIN, self.name)}, name=self.name)

    def notify(self, message: str = "", lang: str = "en-us", **kwargs: Any) -> None:
        """Notify by speaking a message."""
        self.client.emit(Message("speak", {"utterance": message, "lang": lang}))

    def get_volume(self) -> None:
        """Trigger OVOS get volume response."""
        self.client.emit(Message("mycroft.volume.get"))

    def set_volume(self, value: float) -> None:
        """Set OVOS device volume."""
        self.client.emit(Message("mycroft.volume.set", {"percent": value}))

    def get_brightness(self) -> None:
        """Trigger OVOS get brightness response."""
        self.client.emit(Message("phal.brightness.control.get"))

    def set_brightness(self, value: float) -> None:
        """Set OVOS device brightness."""
        self.client.emit(Message("phal.brightness.control.set", {"brightness": value}))
        # Trigger read. This is not auto-triggered like volume does
        self.get_brightness()

    def on_volume_get_response(self, callback: Callable[[Message], None]) -> None:
        """Call callback when OVOS device's volume changes."""
        self.client.on("mycroft.volume.get.response", callback)

    def on_brightness_get_response(self, callback: Callable[[Message], None]) -> None:
        """Call callback when OVOS device's brightness changes."""
        self.client.on("phal.brightness.control.get.response", callback)

    def unload(self) -> None:
        """Close connection."""
        self.client.close()
