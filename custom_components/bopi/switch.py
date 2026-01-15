"""Switch platform for BoPi integration.

Provides switch entities for controlling BoPi relays and pump/light equipment.
"""

from __future__ import annotations

from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import BoPiCoordinator


async def async_setup_entry(
    hass: HomeAssistant,  # pylint: disable=unused-argument
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up BoPi switch entities.

    Args:
    ----
        hass: Home Assistant instance.
        config_entry: Config entry for BoPi integration.
        async_add_entities: Callback to add new entities.

    """
    coordinator: BoPiCoordinator = config_entry.runtime_data.coordinator

    entities: list[SwitchEntity] = [
        BoPiPoolPumpSwitch(coordinator),
        BoPiPoolLightsSwitch(coordinator),
        BoPiRelay1Switch(coordinator),
        BoPiRelay2Switch(coordinator),
        BoPiRelay3Switch(coordinator),
        BoPiRelay4Switch(coordinator),
    ]

    async_add_entities(entities)


class BoPiSwitchBase(  # pylint: disable=abstract-method
    CoordinatorEntity[BoPiCoordinator], SwitchEntity
):
    """Base class for BoPi switches."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: BoPiCoordinator,
        data_key: str,
        name: str,
        translation_key: str | None = None,
    ) -> None:
        """Initialize BoPi switch.

        Args:
        ----
            coordinator: The data coordinator.
            data_key: Key in coordinator data to use for value.
            name: Human-readable name of the switch.
            translation_key: Translation key for the entity.

        """
        super().__init__(coordinator)
        self._data_key = data_key
        self._attr_name = name
        if translation_key:
            self._attr_translation_key = translation_key

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
    def unique_id(self) -> str:
        """Return unique ID for the switch."""
        return f"{self.coordinator.api.host}_{self._data_key}"

    @property
    def is_on(self) -> bool:
        """Return the state value."""
        if not self.coordinator.data:
            return False

        sensors_state = self.coordinator.data.get("sensors_state")
        if not sensors_state:
            return False

        # Navigate nested structure for status
        parts = self._data_key.split(".")
        obj = sensors_state
        for part in parts:
            obj = getattr(obj, part, None)
            if obj is None:
                return False

        return bool(obj)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on the switch.

        Args:
        ----
            kwargs: Additional arguments (unused for now).

        """
        # TODO: Implement relay turn on functionality  # pylint: disable=fixme

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the switch.

        Args:
        ----
            kwargs: Additional arguments (unused for now).

        """
        # TODO: Implement relay turn off functionality  # pylint: disable=fixme


class BoPiPoolPumpSwitch(BoPiSwitchBase):  # pylint: disable=abstract-method
    """Pool pump control switch."""

    def __init__(self, coordinator: BoPiCoordinator) -> None:
        """Initialize pool pump switch."""
        super().__init__(coordinator, "pool_pump.status", "Pool Pump", "pool_pump")


class BoPiPoolLightsSwitch(BoPiSwitchBase):  # pylint: disable=abstract-method
    """Pool lights control switch."""

    def __init__(self, coordinator: BoPiCoordinator) -> None:
        """Initialize pool lights switch."""
        super().__init__(
            coordinator, "pool_lights.status", "Pool Lights", "pool_lights"
        )


class BoPiRelay1Switch(BoPiSwitchBase):  # pylint: disable=abstract-method
    """Relay 1 control switch."""

    def __init__(self, coordinator: BoPiCoordinator) -> None:
        """Initialize relay 1 switch."""
        super().__init__(coordinator, "relay1.status", "Relay 1", "relay1")


class BoPiRelay2Switch(BoPiSwitchBase):  # pylint: disable=abstract-method
    """Relay 2 control switch."""

    def __init__(self, coordinator: BoPiCoordinator) -> None:
        """Initialize relay 2 switch."""
        super().__init__(coordinator, "relay2.status", "Relay 2", "relay2")


class BoPiRelay3Switch(BoPiSwitchBase):  # pylint: disable=abstract-method
    """Relay 3 control switch."""

    def __init__(self, coordinator: BoPiCoordinator) -> None:
        """Initialize relay 3 switch."""
        super().__init__(coordinator, "relay3.status", "Relay 3", "relay3")


class BoPiRelay4Switch(BoPiSwitchBase):  # pylint: disable=abstract-method
    """Relay 4 control switch."""

    def __init__(self, coordinator: BoPiCoordinator) -> None:
        """Initialize relay 4 switch."""
        super().__init__(coordinator, "relay4.status", "Relay 4", "relay4")
