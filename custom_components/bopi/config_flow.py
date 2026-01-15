"""Config flow for BoPi integration."""

from __future__ import annotations

import logging
from typing import Any

from meetbopi import BoPiClient, BoPiConfigError, BoPiConnectionError, BoPiTimeoutError
import voluptuous as vol

from homeassistant.config_entries import (
    ConfigFlow,
    ConfigFlowResult,
    ConfigEntry,
    OptionsFlow,
)
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_SCAN_INTERVAL, CONF_TIMEOUT
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError

from .const import DEFAULT_SCAN_INTERVAL, DOMAIN, MIN_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST, description={"suggested_value": "10.10.10.1"}): str,
        vol.Required(CONF_PORT, description={"suggested_value": 80}, default=80): int,
        vol.Optional(
            CONF_TIMEOUT, description={"suggested_value": 30}, default=30
        ): int,
    }
)

RECONFIGURE_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_PORT): int,
        vol.Required(CONF_TIMEOUT): int,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:  # pylint: disable=unused-argument
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    try:
        bopi_client = BoPiClient(
            data[CONF_HOST], port=data[CONF_PORT], timeout=data[CONF_TIMEOUT]
        )
    except BoPiConfigError as err:
        # Map field to specific error key for form display
        if err.field == CONF_HOST:
            raise InvalidHost from err
        if err.field == CONF_PORT:
            raise InvalidPort from err
        if err.field == CONF_TIMEOUT:
            raise InvalidTimeout from err
        raise InvalidConfig from err

    try:
        await bopi_client.get_sensors_state()
    except BoPiTimeoutError as err:
        raise ConnectionTimeout from err
    except BoPiConnectionError as err:
        raise CannotConnect from err

    return {"title": f"BoPi ({data[CONF_HOST]})"}


class BoPiConfigFlow(ConfigFlow, domain=DOMAIN):  # pylint: disable=abstract-method
    """Handle a config flow for BoPi integration.

    Manages user setup, reconfiguration, and validation of BoPi devices.
    """

    VERSION = 1
    MINOR_VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> BoPiOptionsFlowHandler:
        """Get the options flow for this handler."""
        return BoPiOptionsFlowHandler()

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
            )

        try:
            info = await validate_input(self.hass, user_input)
        except InvalidHost:
            errors[CONF_HOST] = "invalid_host"
        except InvalidPort:
            errors[CONF_PORT] = "invalid_port"
        except InvalidTimeout:
            errors[CONF_TIMEOUT] = "invalid_timeout"
        except InvalidConfig:
            errors["base"] = "invalid_config"
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except ConnectionTimeout:
            errors["base"] = "connection_timeout"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"

        if errors:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
            )

        await self.async_set_unique_id(info.get("title"))
        self._abort_if_unique_id_configured()
        return self.async_create_entry(title=info["title"], data=user_input)

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle reconfigure step."""
        config_entry = self.hass.config_entries.async_get_entry(
            self.context.get("entry_id", "")
        )
        if not config_entry:
            return self.async_abort(reason="reconfigure_failed")

        errors: dict[str, str] = {}

        if user_input is None:
            return self.async_show_form(
                step_id="reconfigure",
                data_schema=vol.Schema(
                    {
                        vol.Required(
                            CONF_HOST, default=config_entry.data[CONF_HOST]
                        ): str,
                        vol.Required(
                            CONF_PORT, default=config_entry.data[CONF_PORT]
                        ): int,
                        vol.Required(
                            CONF_TIMEOUT, default=config_entry.data[CONF_TIMEOUT]
                        ): int,
                    }
                ),
                errors=errors,
            )

        try:
            reconfigure_data = {**config_entry.data, **user_input}
            await validate_input(self.hass, reconfigure_data)
        except InvalidHost:
            errors[CONF_HOST] = "invalid_host"
        except InvalidPort:
            errors[CONF_PORT] = "invalid_port"
        except InvalidTimeout:
            errors[CONF_TIMEOUT] = "invalid_timeout"
        except InvalidConfig:
            errors["base"] = "invalid_config"
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except ConnectionTimeout:
            errors["base"] = "connection_timeout"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"

        if errors:
            return self.async_show_form(
                step_id="reconfigure",
                data_schema=vol.Schema(
                    {
                        vol.Required(
                            CONF_HOST, default=config_entry.data[CONF_HOST]
                        ): str,
                        vol.Required(
                            CONF_PORT, default=config_entry.data[CONF_PORT]
                        ): int,
                        vol.Required(
                            CONF_TIMEOUT, default=config_entry.data[CONF_TIMEOUT]
                        ): int,
                    }
                ),
                errors=errors,
            )

        return self.async_update_reload_and_abort(
            config_entry,
            data=reconfigure_data,
            reason="reconfigure_successful",
        )


class BoPiOptionsFlowHandler(OptionsFlow):
    """Handles options flow for BoPi integration.

    Manages user configuration options such as polling intervals.
    """

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle options flow."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        # It is recommended to prepopulate options fields with default values if available.
        # These will be the same default values you use on your coordinator for setting variable values
        # if the option has not been set.
        data_schema = vol.Schema(
            {
                vol.Required(
                    CONF_SCAN_INTERVAL,
                    default=self.config_entry.options.get(
                        CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                    ),
                ): (vol.All(vol.Coerce(int), vol.Clamp(min=MIN_SCAN_INTERVAL))),
            }
        )

        return self.async_show_form(step_id="init", data_schema=data_schema)


class InvalidConfig(HomeAssistantError):
    """Error to indicate invalid configuration."""


class InvalidHost(HomeAssistantError):
    """Error to indicate invalid host."""


class InvalidPort(HomeAssistantError):
    """Error to indicate invalid port."""


class InvalidTimeout(HomeAssistantError):
    """Error to indicate invalid timeout."""


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class ConnectionTimeout(HomeAssistantError):
    """Error to indicate there is a timeout."""
