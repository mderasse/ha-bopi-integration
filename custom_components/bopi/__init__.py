"""The BoPi integration.

Provides integration with BoPi sensor controller devices via local HTTP API.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from .coordinator import BoPiCoordinator
from .services import async_setup_services

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.SWITCH]

type BoPiConfigEntry = ConfigEntry[RuntimeData]


@dataclass
class RuntimeData:
    """Class to hold bopi runtime data."""

    coordinator: BoPiCoordinator


async def async_setup_entry(hass: HomeAssistant, config_entry: BoPiConfigEntry) -> bool:
    """Set up BoPi integration from a config entry.

    Args:
    ----
        hass: Home Assistant instance.
        config_entry: Config entry for BoPi integration.

    Returns:
    -------
        True if setup successful.

    """
    coordinator = BoPiCoordinator(hass, config_entry)
    await coordinator.async_config_entry_first_refresh()

    config_entry.runtime_data = RuntimeData(coordinator)

    config_entry.async_on_unload(
        config_entry.add_update_listener(_async_update_listener)
    )

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)

    # Set up services
    await async_setup_services(hass, config_entry.runtime_data)

    return True


async def _async_update_listener(
    hass: HomeAssistant,  # pylint: disable=unused-argument
    config_entry: BoPiConfigEntry,
) -> None:
    """Handle config options update.

    Args:
    ----
        hass: Home Assistant instance.
        config_entry: Config entry that changed.

    """
    coordinator: BoPiCoordinator = config_entry.runtime_data.coordinator
    coordinator.update_interval = coordinator._get_update_interval()  # pylint: disable=protected-access


async def async_unload_entry(
    hass: HomeAssistant, config_entry: BoPiConfigEntry
) -> bool:
    """Unload a config entry.

    Args:
    ----
        hass: Home Assistant instance.
        config_entry: Config entry to unload.

    Returns:
    -------
        True if unload successful.

    """
    return await hass.config_entries.async_unload_platforms(config_entry, PLATFORMS)
