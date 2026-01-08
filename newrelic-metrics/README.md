# New Relic Metrics Home Assistant Addon

This Home Assistant addon allows you to fetch metrics from New Relic using NRQL queries and add them as sensors to your Home Assistant instance.

## Features

- Query New Relic using NRQL (New Relic Query Language)
- Automatically create Home Assistant sensors from query results
- Configurable update intervals
- Support for multiple queries
- Custom units of measurement and icons

## Installation

1. Add this repository to your Home Assistant add-on store
2. Install the "New Relic Metrics" addon
3. Configure the addon with your New Relic API key and account ID
4. Start the addon

## Configuration

### Required Settings

- **api_key**: Your New Relic User API Key (not to be confused with License Key)
- **account_id**: Your New Relic account ID
- **ha_token**: Home Assistant Long-Lived Access Token
- **queries**: List of NRQL queries to execute

### Query Options

Each query supports these parameters:

- **name** (required): Friendly name for the sensor
- **nrql** (required): The NRQL query to execute
- **value_field** (optional): Specific field to extract as sensor value. If not specified, shows all fields as JSON.
- **decimal_places** (optional): Round numeric values to this many decimal places
- **unit_of_measurement** (optional): Unit for the sensor (e.g., "s", "%", "GB")
- **icon** (optional): Material Design Icon (default: "mdi:chart-line")

### Optional Settings

- **update_interval**: How often to update metrics in seconds (default: 300)

### Example Configuration

```yaml
api_key: "NRAK-XXXXXXXXXXXXXXXXXXXXXXXXXX"
account_id: "1234567"
ha_token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
update_interval: 300
queries:
  # Simple query - auto-detects first field as sensor value
  - name: "Transaction Count"
    nrql: "SELECT count(*) FROM Transaction WHERE appName = 'MyApp' SINCE 5 minutes ago"
    icon: "mdi:counter"

  # Specific field extraction with rounding
  - name: "APM Response Time"
    nrql: "SELECT average(duration) FROM Transaction WHERE appName = 'MyApp' SINCE 5 minutes ago"
    value_field: "average"
    decimal_places: 2
    unit_of_measurement: "s"
    icon: "mdi:timer"

  # Multiple fields - extract specific one
  - name: "Error Rate"
    nrql: "SELECT percentage(count(*), WHERE error IS true) as error_pct, count(*) FROM Transaction SINCE 5 minutes ago"
    value_field: "error_pct"
    decimal_places: 1
    unit_of_measurement: "%"
    icon: "mdi:alert-circle"
```

## Getting Your Credentials

### New Relic API Key

1. Log in to New Relic
2. Click on your account name in the top right
3. Go to "API keys"
4. Create a new "User" key (or use an existing one)
5. Copy the key (starts with "NRAK-")

### New Relic Account ID

1. Log in to New Relic
2. Your account ID is visible in the URL when viewing your account
3. Or go to Account Settings to find it

### Home Assistant Token

1. In Home Assistant, click your **username** (bottom left)
2. Scroll to **"Long-Lived Access Tokens"**
3. Click **"Create Token"**
4. Name it "New Relic Metrics Addon"
5. **Copy the token** (you'll only see it once!)

See [GET_HA_TOKEN.md](../GET_HA_TOKEN.md) for detailed instructions with screenshots.

## NRQL Query Tips

- Use `SELECT average(metric)`, `SELECT count(*)`, `SELECT sum(metric)`, etc.
- Add `SINCE X minutes ago` to limit the time range
- Filter with `WHERE` clauses
- The addon will extract the first numeric value from the query result

## Created Sensors

Each query will create a sensor with the entity ID:

```
sensor.newrelic_{query_name}
```

The sensor will include:
- **State**: The primary value from the query result
- **Attributes**: All fields from the query result (prefixed with `nr_`)
- **friendly_name**: "New Relic: {query name}"
- **query**: The NRQL query used
- **icon**: Custom icon if specified
- **unit_of_measurement**: Unit if specified

## Troubleshooting

Check the addon logs for detailed information about query execution and any errors.

Common issues:
- Invalid API key: Ensure you're using a User API key (not License key)
- Query errors: Test your NRQL queries in the New Relic query builder first
- No data: Check that your query returns results in New Relic

## Support

For issues and feature requests, please visit the GitHub repository.
