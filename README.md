# WooCommerce Stats for Home Assistant

A custom Home Assistant integration that uses the WooCommerce API to fetch and display basic statistics for your WooCommerce store, such as total sales, orders, and customers.  

## Features
- Fetch live WooCommerce statistics using the WooCommerce API.
- Displays data in Home Assistant as sensors.
- Supports custom Lovelace dashboard cards for visualization.

---

## Installation

### HACS (Home Assistant Community Store)
1. Open HACS in your Home Assistant instance.
2. Go to **Integrations** → Click on the **+ Explore & Download Repositories** button.
3. Add this repository: `https://github.com/techartdev/woocommerce_stats`.
4. Install the "WooCommerce Stats" integration.

### Manual Installation
1. Download the repository as a ZIP file.
2. Extract the ZIP and copy the `woocommerce_stats` folder to your Home Assistant `custom_components` directory.
3. Restart Home Assistant.

---

## Configuration

### Add to `configuration.yaml`

```yaml
woocommerce_stats:
  url: "https://your-woocommerce-store.com"
  consumer_key: "ck_XXXXXXXXXXXXXXXXXXXXXXXXXXXX"
  consumer_secret: "cs_XXXXXXXXXXXXXXXXXXXXXXXXXXXX"
```

### Integration Setup
1. Restart Home Assistant after adding the configuration.
2. The WooCommerce sensors will automatically be created.

---

## Available Sensors
- `sensor.total_sales`: Total sales from the WooCommerce store.
- `sensor.total_orders`: Total number of orders.
- `sensor.total_customers`: Total number of customers.

---

## Example Dashboard Card

### Simple Table
Add the following YAML to your Lovelace dashboard for a table view:

```yaml
type: entities
title: WooCommerce Live Stats
entities:
  - entity: sensor.total_sales
    name: Total Sales
  - entity: sensor.total_orders
    name: Total Orders
  - entity: sensor.total_customers
    name: Total Customers
```

### Chart (ApexCharts)
Install the **ApexCharts** card via HACS, and use this configuration:

```yaml
type: custom:apexcharts-card
header:
  title: WooCommerce Stats
series:
  - entity: sensor.total_sales
    name: Total Sales
  - entity: sensor.total_orders
    name: Total Orders
update_interval: 10min
```

---

## Troubleshooting
If you encounter issues:
1. Check the Home Assistant logs for any error messages.
2. Verify your WooCommerce API credentials and store URL.
3. Ensure the integration is correctly installed and configured.

---

## License
This project is licensed under the MIT License.
