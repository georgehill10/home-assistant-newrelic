# Quick Local Testing Guide

Follow these steps to test the addon locally in Home Assistant without using GitHub.

## Prerequisites

✓ Home Assistant installed and running
✓ SSH access to Home Assistant (install "Terminal & SSH" addon)
✓ New Relic API key and account ID

## Quick Start (5 steps)

### 1. Run the copy script

From this directory, run:

```bash
./copy-to-ha.sh
```

Enter your Home Assistant IP address when prompted (e.g., `192.168.1.100`).

The script will:
- Test SSH connection
- Create the addon directory
- Copy all files to Home Assistant

### 2. Reload Add-ons

In Home Assistant:
1. Go to **Settings** → **Add-ons**
2. Click **⋮** (three dots in top right)
3. Click **Check for updates**

### 3. Install the Addon

1. Scroll to **Local add-ons** section
2. Click **New Relic Metrics**
3. Click **Install**
4. Wait 1-2 minutes for it to build

### 4. Configure

1. Click the **Configuration** tab
2. Paste your configuration:

```yaml
api_key: "NRAK-your-key-here"
account_id: "your-account-id"
ha_token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
update_interval: 300
queries:
  - name: "test_query"
    nrql: "SELECT count(*) FROM Transaction SINCE 5 minutes ago"
    icon: "mdi:chart-line"
```

3. Click **Save**

### 5. Start and Test

1. Go to **Info** tab
2. Click **Start**
3. Click **Log** tab to see output
4. Go to **Developer Tools** → **States**
5. Search for `sensor.newrelic_test_query`

## Making Changes

After editing code:

```bash
# Copy updated files
./copy-to-ha.sh

# Then in Home Assistant:
# Settings → Add-ons → New Relic Metrics → Rebuild → Restart
```

## Manual Copy (Alternative)

If you prefer to copy manually:

```bash
# One-time copy
scp -r newrelic-metrics root@YOUR_HA_IP:/addons/

# Or with rsync (better for updates)
rsync -av --delete newrelic-metrics/ root@YOUR_HA_IP:/addons/newrelic-metrics/
```

## Troubleshooting

### "Addon not found in local add-ons"

- Run the reload step again
- Check SSH: `ssh root@YOUR_HA_IP "ls -la /addons/newrelic-metrics"`
- Try alternative path: `/config/addons/local/newrelic-metrics`

### "Build failed"

- Check addon logs during installation
- Make sure all files copied correctly
- Check Dockerfile syntax

### "Addon won't start"

- Check the **Log** tab
- Verify your API key and account ID
- Make sure queries are configured

### "No sensors appearing"

- Wait 5 minutes for first update
- Check addon is running (green indicator)
- Check logs for errors
- Verify NRQL query works in New Relic

## File Locations

The addon should be at one of these paths on Home Assistant:

- `/addons/newrelic-metrics/` (default for HA OS)
- `/config/addons/local/newrelic-metrics/` (alternative)

You can check with:
```bash
ssh root@YOUR_HA_IP "ls -la /addons/newrelic-metrics/"
```

## Example Configuration

Here's a working example configuration to test with:

```yaml
api_key: "NRAK-XXXXXXXXXXXXXXXXXXXXXXXXXX"
account_id: "1234567"
update_interval: 300
queries:
  # Test with a simple query first
  - name: "transaction_count"
    nrql: "SELECT count(*) FROM Transaction SINCE 5 minutes ago"
    icon: "mdi:counter"

  # Then add more complex queries
  - name: "avg_response_time"
    nrql: "SELECT average(duration) FROM Transaction WHERE appName = 'YourApp' SINCE 5 minutes ago"
    unit_of_measurement: "s"
    icon: "mdi:timer"
```

## Getting Help

- Check logs: Settings → Add-ons → New Relic Metrics → Log
- Home Assistant logs: Settings → System → Logs
- See INSTALL_LOCAL.md for detailed troubleshooting

## Ready to Publish?

Once everything works locally:

1. Commit to Git:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. Push to GitHub:
   ```bash
   git remote add origin https://github.com/georgehill10/home-assistant-newrelic.git
   git push -u origin main
   ```

3. Update repository.json with your GitHub URL

4. Add repository to Home Assistant
