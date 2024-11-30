# WooCommerce Stats for Home Assistant

A custom Home Assistant integration that uses the WooCommerce API to fetch and display basic statistics for your WooCommerce store, such as total sales, orders, and customers.

---

## Features
- Fetch live WooCommerce statistics using the WooCommerce API.
- Displays data in Home Assistant as sensors.
- Supports custom Lovelace dashboard cards for visualization.
- Easily configurable through the Home Assistant UI.

---

## Installation

### HACS (Home Assistant Community Store)
1. Open HACS in your Home Assistant instance.
2. Go to **Integrations** → Click on the **+ Explore & Download Repositories** button.
3. Add this repository: `https://github.com/techartdev/woocommerce_stats`.
4. Install the "WooCommerce Stats" integration.
5. Restart Home Assistant.

### Manual Installation
1. Download the repository as a ZIP file.
2. Extract the ZIP and copy the `woocommerce_stats` folder to your Home Assistant `custom_components` directory.
3. Restart Home Assistant.

---

## Configuration

### Integration Setup via UI
1. After installation, go to **Settings → Devices & Services → Add Integration**.
2. Search for **WooCommerce Stats**.
3. Enter the following:
   - Your WooCommerce store URL (e.g., `https://your-woocommerce-store.com`).
   - Your API **Consumer Key** and **Consumer Secret**.
4. Complete the setup and restart Home Assistant if necessary.

---

## Available Sensors
The following sensors will be created automatically after setup:
- `sensor.total_sales`: Total sales from the WooCommerce store.
- `sensor.total_orders`: Total number of orders.
- `sensor.total_items`: Total number of items sold.
- `sensor.total_tax`: Total tax collected.
- `sensor.total_shipping`: Total shipping charges.
- `sensor.total_customers`: Total number of customers.

---

## Example Dashboard Cards

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
  - entity: sensor.total_items
    name: Total Items Sold
  - entity: sensor.total_tax
    name: Total Tax
  - entity: sensor.total_shipping
    name: Total Shipping
  - entity: sensor.total_customers
    name: Total Customers
```

### Chart (ApexCharts)
To visualize the data as a chart, install the **ApexCharts** card via HACS and use this configuration:

```yaml
type: custom:apexcharts-card
header:
  title: WooCommerce Stats
series:
  - entity: sensor.total_sales
    name: Total Sales
  - entity: sensor.total_orders
    name: Total Orders
  - entity: sensor.total_items
    name: Items Sold
update_interval: 10min
```

---

## Troubleshooting
If you encounter issues:
1. Check the Home Assistant logs for any error messages:
   - Go to **Settings → System → Logs**.
2. Verify your WooCommerce API credentials:
   - Make sure your **Consumer Key** and **Consumer Secret** have read permissions.
3. Ensure your WooCommerce store URL is correct and accessible via HTTPS.
4. If you're using Cloudflare or a security plugin, allowlist your Home Assistant server's IP or bypass security checks for the WooCommerce REST API.

---

## License
This project is licensed under the MIT License.
