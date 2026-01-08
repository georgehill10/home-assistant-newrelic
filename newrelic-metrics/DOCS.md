# Configuration

## Required Options

### api_key

Your New Relic User API Key. This is different from your License Key.

To get your API key:
1. Log in to New Relic
2. Click on your account name → API keys
3. Create or copy a "User" key (starts with "NRAK-")

### account_id

Your New Relic account ID (numeric).

To find your account ID:
1. Log in to New Relic
2. Check the URL or go to Account Settings

### ha_token

Home Assistant Long-Lived Access Token.

To create a token:
1. Click your username in Home Assistant (bottom left)
2. Scroll to "Long-Lived Access Tokens"
3. Click "Create Token"
4. Name it "New Relic Metrics Addon"
5. Copy the token (very long, starts with "eyJ...")

**Important:** You'll only see the token once, so copy it immediately!

### queries

A list of NRQL queries to execute. Each query should have:

- **name** (required): A friendly name for the metric
- **nrql** (required): The NRQL query to execute
- **value_field** (optional): Specific field name to extract as the sensor state. If omitted, all fields are shown as JSON in the state.
- **decimal_places** (optional): Number of decimal places to round numeric values to (e.g., 2 for "2.45")
- **unit_of_measurement** (optional): Unit for the sensor (e.g., "s", "%", "GB")
- **icon** (optional): Material Design Icon (e.g., "mdi:timer")

## Optional Options

### update_interval

How often to fetch metrics from New Relic, in seconds.

Default: `300` (5 minutes)

## Example Configuration

```yaml
api_key: "NRAK-XXXXXXXXXXXXXXXXXXXXXXXXXX"
account_id: "1234567"
ha_token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
update_interval: 300
queries:
  # Extract specific field with rounding
  - name: "CPU Usage"
    nrql: "SELECT average(cpuPercent) as avg_cpu FROM SystemSample SINCE 5 minutes ago"
    value_field: "avg_cpu"
    decimal_places: 1
    unit_of_measurement: "%"
    icon: "mdi:cpu-64-bit"

  # Auto-detect first field
  - name: "Memory Usage"
    nrql: "SELECT average(memoryUsedBytes) / 1024 / 1024 / 1024 FROM SystemSample SINCE 5 minutes ago"
    decimal_places: 2
    unit_of_measurement: "GB"
    icon: "mdi:memory"

  # Multiple fields - extract specific one
  - name: "Error Free Sessions"
    nrql: "SELECT percentage(count(*), WHERE error IS NULL) as efs, count(*) as total FROM PageView SINCE 1 hour ago"
    value_field: "efs"
    decimal_places: 2
    unit_of_measurement: "%"
    icon: "mdi:check-circle"
```

## NRQL Query Guidelines

### Aggregation Functions

Use aggregation functions to get a single numeric value:
- `average(metric)`
- `count(*)`
- `sum(metric)`
- `max(metric)`
- `min(metric)`
- `percentage(count(*), WHERE condition)`
- `uniqueCount(attribute)`

### Time Range

Always specify a time range:
- `SINCE 5 minutes ago`
- `SINCE 1 hour ago`
- `SINCE 1 day ago`

### Filtering

Use WHERE clauses to filter data:
- `WHERE appName = 'MyApp'`
- `WHERE host LIKE 'prod-%'`
- `WHERE transactionType = 'Web'`

### Example Queries

#### Application Performance Monitoring

```nrql
SELECT average(duration) FROM Transaction WHERE appName = 'MyApp' SINCE 5 minutes ago
```

#### Infrastructure Monitoring

```nrql
SELECT average(diskUsedPercent) FROM StorageSample WHERE mountPoint = '/' SINCE 5 minutes ago
```

#### Browser Monitoring

```nrql
SELECT average(duration) FROM PageView WHERE appName = 'MyWebsite' SINCE 10 minutes ago
```

#### Synthetics Monitoring

```nrql
SELECT percentage(count(*), WHERE result = 'SUCCESS') FROM SyntheticCheck SINCE 1 hour ago
```

## Sensor Entity IDs

Sensors are created with the entity ID format:

```
sensor.newrelic_{name}
```

Where `{name}` is the query name converted to lowercase with spaces and hyphens replaced by underscores.

Examples:
- Query name: "CPU Usage" → Entity ID: `sensor.newrelic_cpu_usage`
- Query name: "Active-Users" → Entity ID: `sensor.newrelic_active_users`

## Sensor Attributes

Each sensor includes these attributes:

- `friendly_name`: "New Relic: {query name}"
- `icon`: Custom icon or default "mdi:chart-line"
- `query`: The NRQL query
- `account_id`: Your New Relic account ID
- `unit_of_measurement`: If specified
- `nr_*`: All fields from the query result

## Using Sensors in Automations

Once created, sensors can be used in automations, scripts, and dashboards:

```yaml
automation:
  - alias: "Alert on High Error Rate"
    trigger:
      - platform: numeric_state
        entity_id: sensor.newrelic_error_rate
        above: 5
    action:
      - service: notify.mobile_app
        data:
          message: "Error rate is high: {{ states('sensor.newrelic_error_rate') }}%"
```

## Troubleshooting

### Addon won't start

Check the logs for error messages. Common causes:
- Missing or invalid API key
- Missing account ID
- Empty queries list

### No sensors appearing

1. Check addon logs for errors
2. Verify your NRQL queries return results in New Relic
3. Ensure the addon is running
4. Wait for the first update cycle to complete

### Query returns no data

1. Test the query in New Relic's query builder
2. Check the time range (`SINCE` clause)
3. Verify filters match your data
4. Check that you have data in the specified time range

### API Authentication Errors

- Ensure you're using a User API key, not a License key
- Verify the API key is active and not expired
- Check that the key has the necessary permissions
