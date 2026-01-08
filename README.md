# New Relic Home Assistant Addons

Monitor your applications and infrastructure with New Relic metrics in Home Assistant!

## Add-ons

### New Relic Metrics

Fetch metrics from New Relic using NRQL queries and display them as Home Assistant sensors.

**Features:**
- Execute any NRQL query against your New Relic account
- Automatically create sensors in Home Assistant
- Extract specific fields with `value_field` parameter
- Round values with `decimal_places` parameter
- Multiple queries support
- Custom icons and units of measurement

## Quick Start

### Installation

1. Navigate to **Supervisor** → **Add-on Store** in Home Assistant
2. Click **⋮** (three dots) → **Repositories**
3. Add: `https://github.com/georgehill10/home-assistant-newrelic`
4. Find **New Relic Metrics** and click **Install**

### Configuration

```yaml
api_key: "NRAK-your-newrelic-api-key"
account_id: "your-account-id"
ha_token: "your-home-assistant-token"
update_interval: 300
queries:
  - name: "Error Free Sessions"
    nrql: "SELECT percentage(count(*), WHERE error IS NULL) as efs FROM PageView SINCE 1 hour ago"
    value_field: "efs"
    decimal_places: 2
    unit_of_measurement: "%"
    icon: "mdi:check-circle"
```

See [Quick Start Guide](QUICKSTART.md) for detailed setup instructions.

## Getting Credentials

### New Relic API Key

1. Log in to [New Relic](https://one.newrelic.com)
2. Click your profile → **API keys**
3. Create a new **User** key (starts with `NRAK-`)

### Home Assistant Token

1. Click your username in Home Assistant
2. Scroll to **Long-Lived Access Tokens**
3. **Create Token**
4. Copy the token

See [GET_HA_TOKEN.md](GET_HA_TOKEN.md) for detailed instructions.

## Documentation

- [Quick Start Guide](QUICKSTART.md) - Get started in 5 minutes
- [Configuration Guide](newrelic-metrics/DOCS.md) - Detailed configuration options
- [Local Installation](INSTALL_LOCAL.md) - Install locally for development
- [Token Setup](GET_HA_TOKEN.md) - How to create Home Assistant token

## Example Queries

### Application Monitoring
```yaml
- name: "Response Time"
  nrql: "SELECT average(duration) FROM Transaction SINCE 5 minutes ago"
  decimal_places: 3
  unit_of_measurement: "s"
```

### Infrastructure Monitoring
```yaml
- name: "CPU Usage"
  nrql: "SELECT average(cpuPercent) FROM SystemSample SINCE 5 minutes ago"
  decimal_places: 1
  unit_of_measurement: "%"
```

### Custom Metrics
```yaml
- name: "Active Users"
  nrql: "SELECT uniqueCount(userId) FROM PageView SINCE 1 hour ago"
```

## Support

- **Issues**: [GitHub Issues](https://github.com/georgehill10/home-assistant-newrelic/issues)
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT License - See [LICENSE](LICENSE)
