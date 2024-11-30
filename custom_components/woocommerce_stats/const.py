DOMAIN = "woocommerce_stats"
PLATFORMS = ["sensor"]
DEFAULT_SCAN_INTERVAL = 600  # 10 minutes
SENSORS = [
    {"key": "sales", "name": "Total Sales", "unit": "USD", "icon": "mdi:currency-usd"},
    {"key": "orders", "name": "Total Orders", "unit": "orders", "icon": "mdi:cart"},
]