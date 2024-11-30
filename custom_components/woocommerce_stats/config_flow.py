import logging
from typing import Any

import voluptuous as vol
from woocommerce import API
from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect to WooCommerce."""
    from woocommerce import API

    # Initialize the WooCommerce API client
    wc_api = API(
        url=data["url"],
        consumer_key=data["consumer_key"],
        consumer_secret=data["consumer_secret"],
        version="wc/v3"
    )

    try:
        # Attempt to fetch basic data from the API
        response = wc_api.get("reports/sales").json()

        # Check if the response is valid
        if not isinstance(response, dict):
            _LOGGER.error("Invalid response format: %s", response)
            raise CannotConnect("Invalid response format from WooCommerce API.")

        # Check for specific error codes or missing fields
        if "sales" not in response or "orders" not in response:
            _LOGGER.error("Expected fields missing in response: %s", response)
            raise CannotConnect("Unexpected response format from WooCommerce API.")

    except CannotConnect as err:
        # Re-raise custom errors
        raise err
    except Exception as err:
        # Log and raise unexpected errors
        _LOGGER.exception("Unexpected error during WooCommerce API validation: %s", err)
        raise CannotConnect("An unexpected error occurred.") from err

    # Return validated data (e.g., store name) for creating the config entry
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