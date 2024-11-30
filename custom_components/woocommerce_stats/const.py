DOMAIN = "woocommerce_stats"
COORDINATOR = "coordinator"
PLATFORMS = ["sensor"]
ATTRIBUTION = "Data provided by WooCommerce API"
DEFAULT_SCAN_INTERVAL = 600  # Default update interval in seconds

# Define sensor descriptions
SENSORS = [
    {"key": "total_sales", "name": "Total Sales", "unit": "USD", "icon": "mdi:currency-usd"},
    {"key": "total_orders", "name": "Total Orders", "unit": "orders", "icon": "mdi:cart"},
    {"key": "total_items", "name": "Total Items Sold", "unit": "items", "icon": "mdi:package-variant-closed"},
    {"key": "total_tax", "name": "Total Tax", "unit": "USD", "icon": "mdi:currency-usd"},
    {"key": "total_shipping", "name": "Total Shipping", "unit": "USD", "icon": "mdi:truck"},
    {"key": "total_customers", "name": "Total Customers", "unit": "customers", "icon": "mdi:account-group"},
]
