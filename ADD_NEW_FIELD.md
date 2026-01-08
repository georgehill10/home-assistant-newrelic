# Adding ha_token Field to Existing Configuration

## The Problem

When you have an existing saved configuration, Home Assistant won't automatically show new fields added to the schema. You need to manually add them.

## Solution: Edit Configuration in YAML Mode

### Option 1: Edit in UI (YAML Mode)

1. Go to **Settings** → **Add-ons** → **New Relic Metrics**
2. Click **Configuration** tab
3. Toggle to **YAML mode** (click the three dots ⋮ in the top right, or look for "Edit in YAML" toggle)
4. You should see your current config in YAML format:

```yaml
api_key: "NRAK-..."
account_id: "1234567"
queries:
  - name: "tvos_app_load"
    nrql: "..."
update_interval: 300
```

5. **Add the ha_token line**:

```yaml
api_key: "NRAK-..."
account_id: "1234567"
ha_token: "PASTE_YOUR_TOKEN_HERE"
queries:
  - name: "tvos_app_load"
    nrql: "..."
update_interval: 300
```

6. Click **Save**
7. **Restart** the addon

### Option 2: Edit Config File via SSH

If you can't find YAML mode, edit the config file directly:

1. SSH into Home Assistant
2. Find your addon's config file:

```bash
# Find the addon data directory
ls -la /data/addons/data/

# Look for a directory named something like:
# a0d7b954_newrelic_metrics or similar

# Edit the options.json file
vi /data/addons/data/[addon-directory]/options.json
```

3. It will look like:

```json
{
  "api_key": "NRAK-...",
  "account_id": "1234567",
  "queries": [...],
  "update_interval": 300
}
```

4. Add the ha_token field:

```json
{
  "api_key": "NRAK-...",
  "account_id": "1234567",
  "ha_token": "YOUR_TOKEN_HERE",
  "queries": [...],
  "update_interval": 300
}
```

5. Save and exit
6. Restart the addon from the UI

### Option 3: Delete Saved Config (Fresh Start)

If you want to start fresh:

1. SSH into Home Assistant
2. Find and delete the saved config:

```bash
# Find the addon directory
ls -la /data/addons/data/

# Remove the config file (replace [addon-directory] with actual name)
rm /data/addons/data/[addon-directory]/options.json
```

3. In Home Assistant UI, the Configuration tab should now show all fields including ha_token
4. Configure from scratch

## How to Get Your Home Assistant Token

Before adding it, create the token:

1. Click your **username** (bottom left in Home Assistant)
2. Scroll to **"Long-Lived Access Tokens"**
3. Click **"Create Token"**
4. Name: "New Relic Metrics Addon"
5. **Copy the token** (starts with "eyJ...")

## Complete Example Configuration

```yaml
api_key: "NRAK-XXXXXXXXXXXXXXXXXXXXXXXXXX"
account_id: "1234567"
ha_token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJmYWU0ZTBjZTQzZjI0MTIzYmM1NDQ0NjM4ZmU5YjE4MCIsImlhdCI6MTY3NzY4MjEyMCwiZXhwIjoxOTkzMDQyMTIwfQ.VeryLongTokenStringHere"
update_interval: 300
queries:
  - name: "tvos_app_load"
    nrql: "SELECT count(*) FROM Transaction WHERE appName = 'MyApp' SINCE 5 minutes ago"
    icon: "mdi:chart-line"
```

Save → Restart → Check Logs!
