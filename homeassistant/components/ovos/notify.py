"""OpenVoiceOS (OVOS) and Neon AI notification platform."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.notify import BaseNotificationService
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


def get_service(
    hass: HomeAssistant,
    config: ConfigType,
    discovery_info: DiscoveryInfoType | None = None,
) -> OvosNotificationService:
    """Get the OVOS notification service."""
    return OvosNotificationService(hass.data[DOMAIN])


class OvosNotificationService(BaseNotificationService):
    """The OVOS Notification Service."""

    def __init__(self, config: dict[str, Any]) -> None:
        """Initialize the service."""
        self.config = config

    def send_message(
        self, message: str = "", lang: str = "en-us", **kwargs: Any
    ) -> None:
        """Send a message to OVOS/Neon to speak on instance."""
        for _entry_id, entity in self.config["entries"].items():
            try:
                entity.notify(message, lang, **kwargs)
            except ConnectionRefusedError:
                _LOGGER.error("Could not reach this instance of OVOS")
            except ValueError:
                _LOGGER.error("Error from OVOS messagebus")
