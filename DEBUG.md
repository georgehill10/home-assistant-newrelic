# Debugging "This add-on has no configuration"

If you see this message, follow these steps:

## Step 1: Verify Files Copied Correctly

SSH into Home Assistant and check:

```bash
ssh root@YOUR_HA_IP
ls -la /addons/newrelic-metrics/
cat /addons/newrelic-metrics/config.yaml
```

Make sure `config.yaml` exists and contains the schema section.

## Step 2: Check Home Assistant Logs

In Home Assistant:
1. **Settings** → **System** → **Logs**
2. Look for errors related to the addon or config parsing

Or via SSH:
```bash
ha su logs
```

## Step 3: Rebuild the Addon

1. **Settings** → **Add-ons** → **New Relic Metrics**
2. Click **Rebuild** (not just Restart)
3. Wait for rebuild to complete
4. Refresh your browser (hard refresh: Ctrl+Shift+R or Cmd+Shift+R)

## Step 4: Check Addon Info

Click on the **Info** tab and verify:
- Version shows "1.0.0"
- The description appears

## Step 5: Try Uninstall/Reinstall

1. **Uninstall** the addon
2. Go to **Add-on Store** → **⋮** → **Reload**
3. Find the addon in **Local add-ons**
4. **Install** again

## Alternative: Use JSON Configuration

If the YAML configuration UI doesn't work, you can configure via JSON:

1. Enable **Show in sidebar** on the Info tab
2. SSH into Home Assistant
3. Create the config file manually:

```bash
cat > /data/addons/data/[addon-slug]/options.json << 'EOF'
{
  "api_key": "NRAK-XXXXXXXXXXXXXXXXXXXXXXXXXX",
  "account_id": "1234567",
  "update_interval": 300,
  "queries": [
    {
      "name": "test_query",
      "nrql": "SELECT count(*) FROM Transaction SINCE 5 minutes ago",
      "icon": "mdi:chart-line"
    }
  ]
}
EOF
```

Find the correct addon slug:
```bash
ls -la /data/addons/data/
```

Look for a directory related to `newrelic_metrics`.

## Step 6: Check Supervisor Version

Old Home Assistant versions might have issues with complex schemas.

Check your version:
- **Settings** → **About** → Core version

Minimum recommended: 2023.1.0 or newer

## Still Not Working?

Try simplifying the config.yaml temporarily to test:

```yaml
name: New Relic Metrics
version: "1.0.0"
slug: newrelic_metrics
description: Fetch metrics from New Relic and add them as sensors to Home Assistant
arch:
  - amd64
init: false
hassio_api: true
hassio_role: default
options:
  test: "hello"
schema:
  test: str
```

If this works, the issue is with the list schema for queries.

## Report Back

Let me know:
1. What you see in the logs
2. Your Home Assistant version
3. Whether the simplified config works
