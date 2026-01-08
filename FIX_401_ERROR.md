# Fix for 401 Unauthorized Error

## What Changed

The addon now requires a **Home Assistant Long-Lived Access Token** to create sensors. This is because the SUPERVISOR_TOKEN doesn't have permission to update entity states directly.

## What You Need to Do

### Step 1: Create a Home Assistant Token

1. In Home Assistant, click your **username** in the bottom left sidebar
2. Scroll down to **"Long-Lived Access Tokens"**
3. Click **"Create Token"**
4. Name it: **"New Relic Metrics Addon"**
5. Click **"OK"**
6. **Copy the entire token** (it's very long, starts with "eyJ...")
   - ⚠️ You'll only see it once, so copy it now!

### Step 2: Update Your Addon Files

Run the copy script to update the addon:

```bash
cd /Users/georgehill/dev/home-assistant-NR
./copy-to-ha.sh
```

### Step 3: Update Your Configuration

1. Go to **Settings** → **Add-ons** → **New Relic Metrics**
2. Click **Rebuild** (important - this rebuilds with the new code)
3. Wait for rebuild to complete
4. Click **Configuration** tab
5. Add the `ha_token` field:

```yaml
api_key: "NRAK-your-newrelic-key"
account_id: "your-account-id"
ha_token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ..."  # Paste your token here
update_interval: 300
queries:
  - name: "tvos_app_load"
    nrql: "YOUR NRQL QUERY HERE"
    icon: "mdi:chart-line"
```

6. Click **Save**

### Step 4: Restart the Addon

1. Click **Info** tab
2. Click **Restart**
3. Check the **Log** tab

You should now see:

```
New Relic Metrics addon started
Home Assistant token configured
Processing query: tvos_app_load
Updated sensor sensor.newrelic_tvos_app_load with state: 123
```

### Step 5: Verify Sensors

1. Go to **Developer Tools** → **States**
2. Search for `sensor.newrelic_`
3. Your sensors should appear!

## Security Note

- The token has full access to your Home Assistant
- Keep it secret and secure
- Don't share it or commit it to git
- You can revoke it anytime from your profile

## Troubleshooting

### "Home Assistant token not configured" error

- Make sure you added `ha_token:` to your configuration
- Check that the token is on one line (no line breaks)
- Verify you copied the entire token

### Still getting 401 errors

- Make sure you clicked **Rebuild** (not just Restart)
- Create a new token and try again
- Check the logs for more details

### Lost the token?

- Go to your profile
- Delete the old token
- Create a new one
- Update the addon configuration

## Need Help?

See [GET_HA_TOKEN.md](GET_HA_TOKEN.md) for detailed instructions on creating the token.
