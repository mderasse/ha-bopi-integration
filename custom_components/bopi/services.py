"""Services for BoPi integration."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from homeassistant.core import HomeAssistant, ServiceCall

from .const import DOMAIN, SERVICE_REFRESH

if TYPE_CHECKING:
    from . import RuntimeData

_LOGGER = logging.getLogger(__name__)


async def async_setup_services(hass: HomeAssistant, runtime_data: RuntimeData) -> None:
    """Set up BoPi services.

    Args:
    ----
        hass: Home Assistant instance.
        runtime_data: Runtime data containing coordinator.

    """

    async def handle_refresh(
        call: ServiceCall,  # pylint: disable=unused-argument
    ) -> None:
        """Handle refresh service call.

        Args:
        ----
            call: Service call object.

        """
        await runtime_data.coordinator.async_request_refresh()
        _LOGGER.debug("BoPi sensor refresh forced")

    # Only register if not already registered
    if not hass.services.has_service(DOMAIN, SERVICE_REFRESH):
        hass.services.async_register(
            DOMAIN,
            SERVICE_REFRESH,
            handle_refresh,
        )
