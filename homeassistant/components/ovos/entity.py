"""OVOS Entry wrapper."""
from collections.abc import Callable
import logging
from typing import Any, Optional

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

    def emit(self, message_type: str, data: Optional[dict[str, Any]] = None) -> None:
        """Send message to bus."""
        if data is None:
            data = {}

        self.client.emit(Message(message_type, data))

    def on(self, message_type: str, callback: Callable[[Message], None]) -> None:
        """Subscribe callback to event type."""
        self.client.on(message_type, callback)

    def unload(self) -> None:
        """Close connection."""
        self.client.close()
