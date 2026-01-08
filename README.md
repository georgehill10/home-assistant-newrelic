# Home Assistant New Relic Addons Repository

This repository contains Home Assistant addons for integrating New Relic monitoring into your Home Assistant instance.

## Addons

### New Relic Metrics

Fetch metrics from New Relic using NRQL queries and add them as sensors to Home Assistant.

**Features:**
- Query New Relic using NRQL (New Relic Query Language)
- Automatically create Home Assistant sensors from query results
- Configurable update intervals
- Support for multiple queries
- Custom units of measurement and icons

## Installation

### Method 1: Add Repository to Home Assistant

1. Navigate to **Supervisor** → **Add-on Store** in your Home Assistant instance
2. Click the **⋮** (three dots) in the top right corner
3. Select **Repositories**
4. Add this repository URL:
   ```
   https://github.com/georgehill10/home-assistant-newrelic
   ```
5. Click **Add**
6. Close the repositories dialog
7. Scroll down to find "New Relic Metrics" addon
8. Click on it and then click **Install**

### Method 2: Manual Installation (Development)

1. Copy the `newrelic-metrics` folder to your Home Assistant addons directory:
   ```
   /addons/newrelic-metrics/
   ```
2. Restart Home Assistant or reload addons
3. Install the addon from the Supervisor panel

## Configuration

After installation, configure the addon with your New Relic credentials:

```yaml
api_key: "NRAK-XXXXXXXXXXXXXXXXXXXXXXXXXX"
account_id: "1234567"
update_interval: 300
queries:
  - name: "App Response Time"
    nrql: "SELECT average(duration) FROM Transaction WHERE appName = 'MyApp' SINCE 5 minutes ago"
    unit_of_measurement: "s"
    icon: "mdi:timer"
  - name: "Error Rate"
    nrql: "SELECT percentage(count(*), WHERE error IS true) FROM Transaction WHERE appName = 'MyApp' SINCE 5 minutes ago"
    unit_of_measurement: "%"
    icon: "mdi:alert-circle"
```

See the [addon documentation](newrelic-metrics/DOCS.md) for detailed configuration options.

## Getting Your New Relic Credentials

### API Key

1. Log in to [New Relic](https://one.newrelic.com)
2. Click on your account name in the top right
3. Go to **API keys**
4. Create a new **User** key (or use an existing one)
5. Copy the key (starts with "NRAK-")

**Important:** Use a User API key, not a License key.

### Account ID

1. Log in to New Relic
2. Your account ID is visible in the URL when viewing your account
3. Or go to **Account Settings** to find it

## Usage Examples

### Monitor Application Performance

```yaml
queries:
  - name: "API Response Time"
    nrql: "SELECT average(duration) FROM Transaction WHERE appName = 'MyAPI' SINCE 5 minutes ago"
    unit_of_measurement: "s"
    icon: "mdi:timer"
```

### Monitor Infrastructure

```yaml
queries:
  - name: "Server CPU Usage"
    nrql: "SELECT average(cpuPercent) FROM SystemSample WHERE hostname = 'myserver' SINCE 5 minutes ago"
    unit_of_measurement: "%"
    icon: "mdi:cpu-64-bit"
```

### Monitor Website Traffic

```yaml
queries:
  - name: "Active Users"
    nrql: "SELECT uniqueCount(session) FROM PageView SINCE 1 hour ago"
    icon: "mdi:account-multiple"
```

## Using Sensors in Home Assistant

Once configured, sensors will be created with entity IDs like:
- `sensor.newrelic_api_response_time`
- `sensor.newrelic_server_cpu_usage`
- `sensor.newrelic_active_users`

### Example Automation

```yaml
automation:
  - alias: "Alert on High Response Time"
    trigger:
      - platform: numeric_state
        entity_id: sensor.newrelic_api_response_time
        above: 2
    action:
      - service: notify.mobile_app
        data:
          message: "API response time is high: {{ states('sensor.newrelic_api_response_time') }}s"
```

### Example Dashboard Card

```yaml
type: entities
title: New Relic Metrics
entities:
  - sensor.newrelic_api_response_time
  - sensor.newrelic_error_rate
  - sensor.newrelic_active_users
```

## NRQL Query Examples

### APM (Application Performance Monitoring)

```nrql
# Average response time
SELECT average(duration) FROM Transaction WHERE appName = 'MyApp' SINCE 5 minutes ago

# Error percentage
SELECT percentage(count(*), WHERE error IS true) FROM Transaction SINCE 5 minutes ago

# Requests per minute
SELECT rate(count(*), 1 minute) FROM Transaction SINCE 5 minutes ago

# Slowest transactions
SELECT max(duration) FROM Transaction SINCE 5 minutes ago
```

### Infrastructure

```nrql
# CPU usage
SELECT average(cpuPercent) FROM SystemSample WHERE hostname = 'myserver' SINCE 5 minutes ago

# Memory usage (GB)
SELECT average(memoryUsedBytes) / 1024 / 1024 / 1024 FROM SystemSample SINCE 5 minutes ago

# Disk usage percentage
SELECT average(diskUsedPercent) FROM StorageSample WHERE mountPoint = '/' SINCE 5 minutes ago

# Network throughput (Mbps)
SELECT average(receiveBytesPerSecond) / 1024 / 1024 * 8 FROM NetworkSample SINCE 5 minutes ago
```

### Browser (Real User Monitoring)

```nrql
# Page load time
SELECT average(duration) FROM PageView WHERE appName = 'MyWebsite' SINCE 10 minutes ago

# Unique visitors
SELECT uniqueCount(session) FROM PageView SINCE 1 hour ago

# Page views
SELECT count(*) FROM PageView SINCE 1 hour ago
```

### Synthetics

```nrql
# Uptime percentage
SELECT percentage(count(*), WHERE result = 'SUCCESS') FROM SyntheticCheck SINCE 1 hour ago

# Average check duration
SELECT average(duration) FROM SyntheticCheck WHERE monitorName = 'MyMonitor' SINCE 1 hour ago
```

## Troubleshooting

### Addon won't start

Check the addon logs. Common issues:
- Missing or invalid API key
- Missing account ID
- No queries configured

### No sensors appearing

1. Check addon logs for errors
2. Verify NRQL queries work in New Relic's query builder
3. Ensure the addon is running
4. Wait for the first update cycle

### Query errors

- Test queries in New Relic first
- Ensure aggregation functions return single values
- Check time ranges with `SINCE` clauses
- Verify data exists for your queries

## Support

For issues, feature requests, or contributions:
- Create an issue on GitHub
- Check existing issues for solutions
- Review the [addon documentation](newrelic-metrics/DOCS.md)

## License

MIT License - See LICENSE file for details

## Changelog

### Version 1.0.0
- Initial release
- Support for NRQL queries
- Automatic sensor creation
- Configurable update intervals
- Custom units and icons
