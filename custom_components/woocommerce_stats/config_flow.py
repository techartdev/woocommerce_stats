import logging
from typing import Any

import voluptuous as vol
import aiohttp
import asyncio
from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect to WooCommerce."""
    url = f"{data['url']}/wp-json/wc/v3/reports/sales"
    auth = aiohttp.BasicAuth(data["consumer_key"], data["consumer_secret"])

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, auth=auth) as response:
                if response.status == 401:
                    _LOGGER.error("Invalid WooCommerce API credentials.")
                    raise InvalidAuth("Invalid WooCommerce API credentials.")
                if response.status != 200:
                    _LOGGER.error(
                        "Failed to connect to WooCommerce API. HTTP Status: %s", response.status
                    )
                    raise CannotConnect(
                        f"Failed to connect to WooCommerce API. HTTP Status: {response.status}"
                    )
                result = await response.json()
                if not isinstance(result, dict):
                    raise CannotConnect("Unexpected response format from WooCommerce API.")
        except aiohttp.ClientError as err:
            _LOGGER.error("Error communicating with WooCommerce API: %s", err)
            raise CannotConnect(f"Error communicating with WooCommerce API: {err}") from err

    return {"store_name": "WooCommerce Store"}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for WooCommerce Stats."""

    VERSION = 1

    def __init__(self):
        """Initialize the config flow."""
        self._reauth_entry = None

    async def async_step_user(self, user_input: dict[str, Any] = None) -> config_entries.FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                validated_data = await validate_input(self.hass, user_input)
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except CannotConnect as err:
                _LOGGER.error("Connection failed: %s", err)
                errors["base"] = "cannot_connect"
            except Exception as err:
                _LOGGER.exception("Unexpected error during validation: %s", err)
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=validated_data["store_name"],
                    data=user_input
                )

        # Input form schema
        schema = vol.Schema({
            vol.Required("url", default="https://yourstore.com"): str,
            vol.Required("consumer_key"): str,
            vol.Required("consumer_secret"): str,
        })

        return self.async_show_form(
            step_id="user", data_schema=schema, errors=errors
        )
    

    async def async_step_reauth(self, user_input: dict[str, Any] = None) -> config_entries.FlowResult:
        """Handle re-authentication."""
        self._reauth_entry = self.hass.config_entries.async_get_entry(
            self.context["entry_id"]
        )
        return await self.async_step_user()

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options for WooCommerce Stats."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        # Define options schema
        schema = vol.Schema({
            vol.Optional(
                "update_interval",
                default=self.config_entry.options.get("update_interval", 600),
            ): vol.All(vol.Coerce(int), vol.Range(min=60, max=3600)),
        })

        return self.async_show_form(step_id="init", data_schema=schema)


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect to WooCommerce."""

    def __init__(self, message="Cannot connect to WooCommerce API."):
        super().__init__(message)


class InvalidAuth(HomeAssistantError):
    """Error to indicate invalid authentication."""