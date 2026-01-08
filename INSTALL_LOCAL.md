# Installing Addon Locally in Home Assistant

This guide shows you how to install and test the New Relic Metrics addon locally without using GitHub or Docker registries.

## Prerequisites

- Home Assistant installed (OS, Supervised, or Container)
- SSH or direct access to your Home Assistant instance
- New Relic API key and account ID

## Installation Steps

### Step 1: Copy Addon to Home Assistant

#### For Home Assistant OS / Supervised

1. **Enable SSH access** (if not already done):
   - Install the "Terminal & SSH" or "Advanced SSH & Web Terminal" addon
   - Start the addon and connect

2. **Create local addons directory** (if it doesn't exist):
   ```bash
   mkdir -p /addons
   ```

3. **Copy the addon folder** from your development machine:

   **Option A - Using SCP:**
   ```bash
   # From your development machine (Mac/Linux)
   cd /Users/georgehill/dev/home-assistant-NR
   scp -r newrelic-metrics root@YOUR_HOME_ASSISTANT_IP:/addons/
   ```

   **Option B - Using rsync (better for updates):**
   ```bash
   # From your development machine
   cd /Users/georgehill/dev/home-assistant-NR
   rsync -av --delete newrelic-metrics/ root@YOUR_HOME_ASSISTANT_IP:/addons/newrelic-metrics/
   ```

   **Option C - Manual copy via Samba/SMB:**
   - Enable Samba share addon in Home Assistant
   - Connect to your Home Assistant share from your computer
   - Navigate to the `addons` folder
   - Copy the `newrelic-metrics` folder there

   **Option D - Using add-ons directory in config:**
   Some installations use `/config/addons/local/`:
   ```bash
   # SSH into Home Assistant first
   mkdir -p /config/addons/local
   # Then copy from your machine
   scp -r newrelic-metrics root@YOUR_HOME_ASSISTANT_IP:/config/addons/local/
   ```

#### For Home Assistant Container (Docker)

1. **Find your Home Assistant config directory** (where configuration.yaml is)

2. **Create addons directory:**
   ```bash
   mkdir -p /path/to/homeassistant/config/addons/local
   ```

3. **Copy the addon:**
   ```bash
   cp -r /Users/georgehill/dev/home-assistant-NR/newrelic-metrics \
        /path/to/homeassistant/config/addons/local/
   ```

### Step 2: Reload Add-on Store

1. In Home Assistant, go to **Settings** → **Add-ons**
2. Click the **⋮** (three dots) in the top right
3. Click **Check for updates** or **Reload**

### Step 3: Find Your Local Addon

1. Scroll down to the **Local add-ons** section
2. You should see **New Relic Metrics**
3. Click on it

### Step 4: Install the Addon

1. Click **Install**
2. Home Assistant will build the Docker image locally (this may take a few minutes)
3. Wait for the installation to complete

### Step 5: Configure the Addon

1. Go to the **Configuration** tab
2. Add your configuration:

   ```yaml
   api_key: "NRAK-XXXXXXXXXXXXXXXXXXXXXXXXXX"
   account_id: "1234567"
   update_interval: 300
   queries:
     - name: "test_metric"
       nrql: "SELECT count(*) FROM Transaction SINCE 5 minutes ago"
       icon: "mdi:chart-line"
   ```

3. Click **Save**

### Step 6: Start the Addon

1. Go to the **Info** tab
2. Enable **Start on boot** (optional)
3. Enable **Watchdog** (optional)
4. Click **Start**

### Step 7: Check Logs

1. Go to the **Log** tab
2. You should see:
   ```
   New Relic Metrics addon started
   Update interval: 300 seconds
   Number of queries: 1
   Processing query: test_metric
   Updated sensor sensor.newrelic_test_metric with state: 123
   ```

### Step 8: Verify Sensors

1. Go to **Developer Tools** → **States**
2. Search for `sensor.newrelic_`
3. You should see your new sensors!

## Making Changes During Development

When you update the addon code:

1. **Copy the updated files** to Home Assistant (using scp/rsync as above)

2. **Rebuild the addon:**
   - Go to the addon page
   - Click **Rebuild**

3. **Restart the addon:**
   - Click **Restart**

4. **Check logs** for any errors

## Quick Update Script

Save this as `update-addon.sh` in your development directory:

```bash
#!/bin/bash

# Configuration
HA_IP="YOUR_HOME_ASSISTANT_IP"
HA_USER="root"
ADDON_PATH="/addons/newrelic-metrics"

# Sync files
echo "Syncing addon files..."
rsync -av --delete \
  --exclude='.git' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  newrelic-metrics/ ${HA_USER}@${HA_IP}:${ADDON_PATH}/

echo "Done! Now rebuild the addon in Home Assistant."
echo "Go to: Settings → Add-ons → New Relic Metrics → Rebuild"
```

Make it executable:
```bash
chmod +x update-addon.sh
```

Then run it whenever you make changes:
```bash
./update-addon.sh
```

## Troubleshooting

### Addon not appearing in local addons

- Check that the folder is in the correct location (`/addons/` or `/config/addons/local/`)
- Ensure `config.yaml` exists and is valid YAML
- Reload the add-on store
- Check Home Assistant logs

### Build fails

- Check the **Log** tab during installation
- Common issues:
  - Invalid Dockerfile syntax
  - Missing files referenced in Dockerfile
  - Network issues downloading base images

### Addon won't start

- Check the addon **Log** tab
- Common issues:
  - Invalid configuration (missing API key, etc.)
  - Permissions issues with `/data/options.json`
  - Python syntax errors in `newrelic_sensor.py`

### Can't connect to Home Assistant

If using Home Assistant Container, you may need to add the addon to your `docker-compose.yml` or use the Supervisor API endpoint differently.

### Changes not reflected

- Make sure you clicked **Rebuild** after updating files
- Restart the addon after rebuilding
- Check file permissions (should be readable by Home Assistant)

## Directory Structure Reference

Your addon should be at one of these locations:

**Home Assistant OS/Supervised:**
- `/addons/newrelic-metrics/`
- `/config/addons/local/newrelic-metrics/`

**Home Assistant Container:**
- `/path/to/config/addons/local/newrelic-metrics/`

The directory should contain:
```
newrelic-metrics/
├── config.yaml
├── Dockerfile
├── build.yaml
├── run.sh
├── newrelic_sensor.py
├── README.md
└── DOCS.md
```

## Next Steps

Once everything works locally:
1. Commit to Git
2. Push to GitHub
3. Add `image:` field back to `config.yaml` if you want to use registry images
4. Set up GitHub Actions for automated builds
