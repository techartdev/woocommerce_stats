from homeassistant.components.sensor import SensorEntityDescription

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

# Define sensor descriptions
SENSORS = [
    SensorEntityDescription(
        key="total_sales",
        name="Total Sales",
        icon="mdi:currency-usd",
        native_unit_of_measurement="USD",
    ),
        SensorEntityDescription(
        key="net_sales",
        name="Net Sales",
        icon="mdi:currency-usd",
        native_unit_of_measurement="USD",
    ),
    SensorEntityDescription(
        key="total_orders",
        name="Total Orders",
        icon="mdi:cart",
        native_unit_of_measurement="orders",
    ),
    SensorEntityDescription(
        key="total_items",
        name="Total Items Sold",
        icon="mdi:package-variant-closed",
        native_unit_of_measurement="items",
    ),
    SensorEntityDescription(
        key="total_tax",
        name="Total Tax",
        icon="mdi:currency-usd",
        native_unit_of_measurement="USD",
    ),
    SensorEntityDescription(
        key="total_shipping",
        name="Total Shipping",
        icon="mdi:truck",
        native_unit_of_measurement="USD",
    ),
    SensorEntityDescription(
        key="total_customers",
        name="Total Customers",
        icon="mdi:account-group",
        native_unit_of_measurement="customers",
    ),
]
