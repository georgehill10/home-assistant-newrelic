# Force Schema Update - Fix "ha_token Gets Removed" Issue

## The Problem

Home Assistant validates your configuration against the addon's schema. If you add `ha_token` but the addon is still running with the old schema (without `ha_token`), it gets removed when you save.

## Solution: Update in the Correct Order

### Step 1: Copy New Files (Version 1.0.1)

```bash
cd /Users/georgehill/dev/home-assistant-NR
./copy-to-ha.sh
```

### Step 2: Stop the Addon

In Home Assistant:
1. Go to **Settings** → **Add-ons** → **New Relic Metrics**
2. Click **Stop** (if running)

### Step 3: Rebuild with New Schema

1. Click **Rebuild** (this rebuilds with the new config.yaml that includes ha_token)
2. Wait for rebuild to complete (watch the log)
3. You should see it build version **1.0.1** (not 1.0.0)

### Step 4: Verify New Schema

After rebuild:
1. Go to **Info** tab
2. Verify version shows **1.0.1**
3. If still showing 1.0.0, the rebuild didn't pick up the new files

### Step 5: Now Add ha_token

1. Go to **Configuration** tab
2. Switch to **YAML mode** (if available)
3. Add the ha_token field:

```yaml
api_key: "NRAK-..."
account_id: "1234567"
ha_token: "YOUR_LONG_LIVED_TOKEN_HERE"
queries:
  - name: "tvos_app_load"
    nrql: "..."
update_interval: 300
```

4. Click **Save**
5. The field should **NOT** be removed now!

### Step 6: Start the Addon

1. Click **Start**
2. Check **Log** tab
3. Should see: "Home Assistant token configured"
4. Should see: "Updated sensor sensor.newrelic_tvos_app_load with state: X"

## If Version Still Shows 1.0.0

The new files didn't copy properly. Verify:

```bash
# Check version on Home Assistant
ssh root@YOUR_HA_IP "grep 'version:' /addons/newrelic-metrics/config.yaml"
```

Should show: `version: "1.0.1"`

If it shows `1.0.0`, the files didn't copy. Try:

```bash
# Manual copy with rsync
rsync -av --delete newrelic-metrics/ root@YOUR_HA_IP:/addons/newrelic-metrics/
```

Then rebuild again.

## If ha_token Still Gets Removed

The rebuild isn't working properly. Try the nuclear option:

1. **Uninstall** the addon completely
2. **Reload** the add-on store
3. **Install** fresh (it will use version 1.0.1)
4. **Configure** with ha_token from the start

## Alternative: Edit Config File Directly After Rebuild

After rebuilding to version 1.0.1:

1. SSH into Home Assistant:
```bash
ssh root@YOUR_HA_IP
```

2. Find the config directory:
```bash
ls /data/addons/data/
# Look for directory like: a0d7b954_newrelic_metrics
```

3. Edit the options.json:
```bash
vi /data/addons/data/a0d7b954_newrelic_metrics/options.json
```

4. Add ha_token to the JSON:
```json
{
  "api_key": "NRAK-...",
  "account_id": "1234567",
  "ha_token": "YOUR_TOKEN_HERE",
  "queries": [...],
  "update_interval": 300
}
```

5. Save, exit, and restart the addon from UI

This bypasses the UI validation entirely.
