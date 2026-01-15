"""BoPi integration using DataUpdateCoordinator."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from meetbopi import BoPiClient
from meetbopi.exceptions import (
    BoPiConnectionError,
    BoPiTimeoutError,
    BoPiValidationError,
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_HOST,
    CONF_PORT,
    CONF_SCAN_INTERVAL,
    CONF_TIMEOUT,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class BoPiCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator for BoPi integration."""

    data: dict[str, Any]

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize coordinator.

        Args:
        ----
            hass: Home Assistant instance.
            config_entry: Config entry for BoPi integration.

        """
        self.host = config_entry.data[CONF_HOST]
        self.port = config_entry.data[CONF_PORT]
        self.timeout = config_entry.data[CONF_TIMEOUT]
        self._config_entry: ConfigEntry = config_entry

        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN} ({config_entry.unique_id})",
            config_entry=config_entry,
            update_interval=self._get_update_interval(),
        )

        self.api = BoPiClient(self.host, port=self.port, timeout=self.timeout)

    def _get_update_interval(self) -> timedelta:
        """Get the current update interval from config entry options.

        Returns:
        -------
            Update interval as timedelta.

        """
        poll_interval = self._config_entry.options.get(
            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
        )
        return timedelta(seconds=poll_interval)

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from API endpoint.

        Returns:
        -------
            Dictionary containing host and sensor state information.

        Raises:
        ------
            UpdateFailed: If data fetch fails.

        """
        try:
            sensors_state = await self.api.get_sensors_state()
        except BoPiTimeoutError as err:
            raise UpdateFailed(f"Timeout communicating with API: {err}") from err
        except BoPiConnectionError as err:
            raise UpdateFailed(f"Error connecting to API: {err}") from err
        except BoPiValidationError as err:
            raise UpdateFailed(f"Invalid API response: {err}") from err

        return {
            "host": self.api.host,
            "sensors_state": sensors_state,
        }
