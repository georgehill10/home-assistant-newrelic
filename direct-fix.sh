#!/bin/bash

HA_IP="192.168.0.67"

echo "=== Direct Fix for ha_token Issue ==="
echo ""

# Step 1: Find the addon data directory
echo "Step 1: Finding addon config file..."
ADDON_DIR=$(ssh root@${HA_IP} "ls -d /data/addons/data/*newrelic* 2>/dev/null | head -1")

if [ -z "$ADDON_DIR" ]; then
    echo "Could not find addon data directory!"
    echo "Trying alternative locations..."
    ADDON_DIR=$(ssh root@${HA_IP} "find /data -name '*newrelic*' -type d 2>/dev/null | grep addons | head -1")
fi

echo "Found: $ADDON_DIR"
echo ""

# Step 2: Backup current config
echo "Step 2: Backing up current config..."
ssh root@${HA_IP} "cp ${ADDON_DIR}/options.json ${ADDON_DIR}/options.json.backup 2>/dev/null"
echo "Backup created (if file existed)"
echo ""

# Step 3: Show current config
echo "Step 3: Current configuration:"
ssh root@${HA_IP} "cat ${ADDON_DIR}/options.json 2>/dev/null" || echo "No config file found yet"
echo ""

# Step 4: Ask for token
echo "Step 4: Enter your Home Assistant Long-Lived Access Token:"
echo "(Create one: Click your username → Long-Lived Access Tokens → Create Token)"
read -p "Token: " HA_TOKEN

if [ -z "$HA_TOKEN" ]; then
    echo "No token provided. Exiting."
    exit 1
fi

# Step 5: Update config with ha_token
echo ""
echo "Step 5: Adding ha_token to configuration..."
ssh root@${HA_IP} "python3 << 'PYEOF'
import json
import sys

config_file = '${ADDON_DIR}/options.json'

try:
    with open(config_file, 'r') as f:
        config = json.load(f)

    config['ha_token'] = '${HA_TOKEN}'

    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

    print('✓ Successfully added ha_token to config!')
except Exception as e:
    print(f'Error: {e}')
    sys.exit(1)
PYEOF
"

echo ""
echo "Step 6: Verifying updated config..."
ssh root@${HA_IP} "cat ${ADDON_DIR}/options.json | grep -q 'ha_token' && echo '✓ ha_token found in config!' || echo '✗ ha_token not found!'"

echo ""
echo "Done! Now:"
echo "1. Go to Home Assistant → Settings → Add-ons → New Relic Metrics"
echo "2. Click Restart"
echo "3. Check the Log tab"
echo "4. You should see: 'Home Assistant token configured'"
