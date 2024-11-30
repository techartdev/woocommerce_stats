from homeassistant.helpers import config_validation as cv
import voluptuous as vol

DOMAIN = "woocommerce_stats"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required("url"): cv.url,
                vol.Required("consumer_key"): cv.string,
                vol.Required("consumer_secret"): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)
