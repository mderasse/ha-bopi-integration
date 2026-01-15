"""Sensor platform for BoPi integration.

Provides sensor entities for BoPi device sensors accessed via HTTP API.
"""

from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    UnitOfTemperature,
    UnitOfTime,
    UnitOfElectricPotential,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import BoPiCoordinator


SENSOR_DESCRIPTIONS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="temp1",
        translation_key="temp1",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="temp2",
        translation_key="temp2",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="boxtemp",
        translation_key="boxtemp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="boxhumidity",
        translation_key="boxhumidity",
        device_class=SensorDeviceClass.HUMIDITY,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="phvalue",
        translation_key="phvalue",
        device_class=SensorDeviceClass.PH,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    SensorEntityDescription(
        key="redoxvalue",
        translation_key="redoxvalue",
        native_unit_of_measurement=UnitOfElectricPotential.MILLIVOLT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="uptime",
        translation_key="uptime",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # pylint: disable=unused-argument
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up BoPi sensor entities.

    Args:
    ----
        hass: Home Assistant instance.
        config_entry: Config entry for BoPi integration.
        async_add_entities: Callback to add new entities.

    """
    coordinator: BoPiCoordinator = config_entry.runtime_data.coordinator

    async_add_entities(
        BoPiSensor(coordinator, description) for description in SENSOR_DESCRIPTIONS
    )


class BoPiSensor(CoordinatorEntity[BoPiCoordinator], SensorEntity):
    """Representation of a BoPi sensor."""

    _attr_has_entity_name = True

    def __init__(
        self, coordinator: BoPiCoordinator, description: SensorEntityDescription
    ) -> None:
        """Initialize BoPi sensor entity."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.api.host}_{description.key}"
        self._sensor_key = description.key

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
    def native_value(self) -> StateType:
        """Return the state value."""
        if not self.coordinator.data:
            return None

        sensors_state = self.coordinator.data.get("sensors_state")
        if not sensors_state:
            return None

        return getattr(sensors_state, self._sensor_key, None)
