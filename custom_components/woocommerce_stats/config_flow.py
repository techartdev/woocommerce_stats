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
    wc_api = API(
        url=data["url"],
        consumer_key=data["consumer_key"],
        consumer_secret=data["consumer_secret"],
        version="wc/v3"
    )
    try:
        response = wc_api.get("reports/totals").json()
        if not isinstance(response, dict):
            raise CannotConnect
    except Exception as err:
        raise CannotConnect from err

    # Return validated data (e.g., store name) for the entry
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
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception as err:
                _LOGGER.exception("Unexpected exception during validation: %s", err)
                errors["base"] = "unknown"
            else:
                # If re-auth, update the existing entry
                if self._reauth_entry:
                    self.hass.config_entries.async_update_entry(
                        self._reauth_entry, data=user_input
                    )
                    return self.async_abort(reason="reauth_successful")

                # Create a new config entry
                return self.async_create_entry(
                    title=validated_data["store_name"], data=user_input
                )

        # Input form schema
        schema = vol.Schema({
            vol.Required("url", default="https://your-store.com"): str,
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
