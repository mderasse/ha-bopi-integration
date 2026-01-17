"""Switch platform for BoPi integration.

Provides switch entities for controlling BoPi relays and pump/light equipment.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.switch import (
    SwitchEntity,
    SwitchEntityDescription,
)
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import BoPiConfigEntry
from .const import DOMAIN
from .coordinator import BoPiCoordinator


@dataclass(frozen=True, kw_only=True)
class BoPiSwitchEntityDescription(SwitchEntityDescription):
    """Describes a BoPi switch entity."""

    data_key: str


# pylint: disable=unexpected-keyword-arg
SWITCH_DESCRIPTIONS: tuple[BoPiSwitchEntityDescription, ...] = (
    BoPiSwitchEntityDescription(
        key="pool_pump",
        translation_key="pool_pump",
        data_key="pool_pump.status",
        icon="mdi:pump",
    ),
    BoPiSwitchEntityDescription(
        key="pool_lights",
        translation_key="pool_lights",
        data_key="pool_lights.status",
        icon="mdi:lightbulb",
    ),
    BoPiSwitchEntityDescription(
        key="relay1",
        translation_key="relay1",
        data_key="relay1.status",
        icon="mdi:electric-switch",
    ),
    BoPiSwitchEntityDescription(
        key="relay2",
        translation_key="relay2",
        data_key="relay2.status",
        icon="mdi:electric-switch",
    ),
    BoPiSwitchEntityDescription(
        key="relay3",
        translation_key="relay3",
        data_key="relay3.status",
        icon="mdi:electric-switch",
    ),
    BoPiSwitchEntityDescription(
        key="relay4",
        translation_key="relay4",
        data_key="relay4.status",
        icon="mdi:electric-switch",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # pylint: disable=unused-argument
    config_entry: BoPiConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up BoPi switch entities.

    Args:
    ----
        hass: Home Assistant instance.
        config_entry: Config entry for BoPi integration.
        async_add_entities: Callback to add new entities.

    """
    coordinator = config_entry.runtime_data.coordinator

    async_add_entities(
        BoPiSwitch(coordinator, description) for description in SWITCH_DESCRIPTIONS
    )


# pylint: disable=abstract-method
class BoPiSwitch(CoordinatorEntity[BoPiCoordinator], SwitchEntity):
    """Representation of a BoPi switch."""

    _attr_has_entity_name = True
    entity_description: BoPiSwitchEntityDescription

    def __init__(
        self,
        coordinator: BoPiCoordinator,
        description: BoPiSwitchEntityDescription,
    ) -> None:
        """Initialize BoPi switch.

        Args:
        ----
            coordinator: The data coordinator.
            description: Entity description for this switch.

        """
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.api.host}_{description.key}"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.api.host)},
            name="BoPi Controller",
            manufacturer="BoPi",
            model="BoPi Pool Controller",
        )

    @property
    def is_on(self) -> bool:
        """Return the state value."""
        if not self.coordinator.data:
            return False

        sensors_state = self.coordinator.data.get("sensors_state")
        if not sensors_state:
            return False

        # Navigate nested structure for status
        parts = self.entity_description.data_key.split(".")
        obj = sensors_state
        for part in parts:
            obj = getattr(obj, part, None)
            if obj is None:
                return False

        return bool(obj)

    async def async_turn_on(self, **kwargs: Any) -> None:  # noqa: ARG002
        """Turn on the switch.

        Args:
        ----
            kwargs: Additional arguments (unused for now).

        Raises:
        ------
            HomeAssistantError: Switch control is not yet implemented.

        """
        raise HomeAssistantError(
            translation_domain=DOMAIN,
            translation_key="switch_control_not_implemented",
        )

    async def async_turn_off(self, **kwargs: Any) -> None:  # noqa: ARG002
        """Turn off the switch.

        Args:
        ----
            kwargs: Additional arguments (unused for now).

        Raises:
        ------
            HomeAssistantError: Switch control is not yet implemented.

        """
        raise HomeAssistantError(
            translation_domain=DOMAIN,
            translation_key="switch_control_not_implemented",
        )
