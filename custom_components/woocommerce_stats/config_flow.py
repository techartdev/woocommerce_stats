from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN

class WooCommerceConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for WooCommerce Stats."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({
                    vol.Required("url"): str,
                    vol.Required("consumer_key"): str,
                    vol.Required("consumer_secret"): str,
                })
            )

        return self.async_create_entry(title="WooCommerce Stats", data=user_input)
