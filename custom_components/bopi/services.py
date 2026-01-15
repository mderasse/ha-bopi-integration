"""Services for BoPi integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.core import HomeAssistant, ServiceCall

from .const import DOMAIN, SERVICE_REFRESH
from .coordinator import BoPiCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_services(
    hass: HomeAssistant, config_entry_runtime_data: Any
) -> None:
    """Set up BoPi services.

    Args:
    ----
        hass: Home Assistant instance.
        config_entry_runtime_data: Runtime data containing coordinator.

    """

    async def handle_refresh(call: ServiceCall) -> None:  # pylint: disable=unused-argument
        """Handle refresh service call.

        Args:
        ----
            call: Service call object.

        """
        coordinator: BoPiCoordinator = config_entry_runtime_data.coordinator
        await coordinator.async_request_refresh()
        _LOGGER.debug("BoPi sensor refresh forced")

    hass.services.async_register(
        DOMAIN,
        SERVICE_REFRESH,
        handle_refresh,
    )
