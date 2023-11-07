"""OVOS Entry wrapper."""
from typing import Any

from ovos_bus_client import Message, MessageBusClient

from homeassistant.config_entries import ConfigEntry


class Entry:
    """Wrapper of an OVOS entry."""

    def __init__(self, config: ConfigEntry) -> None:
        """Initialize entry and setups connection."""
        self.config = config

        self.client = MessageBusClient(
            host=self.config.data["host"], port=self.config.data["port"]
        )
        self.client.run_in_thread()

    def notify(self, message: str = "", lang: str = "en-us", **kwargs: Any) -> None:
        """Notify by speaking a message."""
        self.client.emit(Message("speak", {"utterance": message, "lang": lang}))

    def unload(self) -> None:
        """Close connection."""
        self.client.close()
