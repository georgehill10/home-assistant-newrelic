# Quick Start Guide

Get your New Relic metrics into Home Assistant in 5 minutes!

## Step 1: Get Your New Relic Credentials

### API Key
1. Go to [New Relic](https://one.newrelic.com)
2. Click your profile → **API keys**
3. Create a new **User** key (starts with `NRAK-`)
4. Copy the key

### Account ID
1. In New Relic, check your URL: `https://one.newrelic.com/nr1-core?account=1234567`
2. The number after `account=` is your account ID

## Step 2: Install the Addon

### Home Assistant

1. Go to **Supervisor** → **Add-on Store**
2. Click **⋮** (top right) → **Repositories**
3. Add: `https://github.com/georgehill10/home-assistant-newrelic`
4. Find **New Relic Metrics** and click **Install**

## Step 3: Configure

Click on the addon and go to the **Configuration** tab:

```yaml
api_key: "NRAK-XXXXXXXXXXXXXXXXXXXXXXXXXX"
account_id: "1234567"
update_interval: 300
queries:
  - name: "Test Query"
    nrql: "SELECT count(*) FROM Transaction SINCE 5 minutes ago"
    icon: "mdi:chart-line"
```

**Important:** Replace with your actual API key and account ID!

## Step 4: Start the Addon

1. Go to the **Info** tab
2. Click **Start**
3. Check the **Log** tab for any errors

## Step 5: Verify Sensors

1. Go to **Developer Tools** → **States**
2. Search for `sensor.newrelic_`
3. You should see your new sensor!

## Example Queries

### Monitor Your Application

```yaml
queries:
  - name: "API Response Time"
    nrql: "SELECT average(duration) FROM Transaction WHERE appName = 'YourApp' SINCE 5 minutes ago"
    unit_of_measurement: "s"
    icon: "mdi:timer"
```

### Monitor Your Server

```yaml
queries:
  - name: "CPU Usage"
    nrql: "SELECT average(cpuPercent) FROM SystemSample WHERE hostname = 'yourserver' SINCE 5 minutes ago"
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

## Troubleshooting

### No sensors appearing?

1. Check addon logs for errors
2. Verify your API key and account ID
3. Test your NRQL query in New Relic first
4. Wait 5 minutes for the first update

### Query errors?

- Ensure your query returns a single numeric value
- Use aggregation: `average()`, `count()`, `sum()`, etc.
- Add a time range: `SINCE 5 minutes ago`
- Test in New Relic's query builder first

### Authentication errors?

- Ensure you're using a **User** API key (starts with `NRAK-`)
- Not a License key or Ingest key
- Check the key is active and has correct permissions

## Next Steps

### Create a Dashboard

```yaml
title: New Relic
cards:
  - type: entities
    title: Application Health
    entities:
      - sensor.newrelic_api_response_time
      - sensor.newrelic_error_rate
      - sensor.newrelic_active_users
```

### Create an Automation

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
          message: "Error rate is {{ states('sensor.newrelic_error_rate') }}%"
```

### Add More Queries

Check [config.example.yaml](newrelic-metrics/config.example.yaml) for more query examples!

## Need Help?

- Check the [full documentation](newrelic-metrics/DOCS.md)
- Review [common issues](README.md#troubleshooting)
- Open a [GitHub issue](https://github.com/georgehill10/home-assistant-newrelic/issues)

Happy monitoring!
