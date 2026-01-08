#!/bin/bash

# Manual update script with verification

echo "Enter your Home Assistant IP address:"
read HA_IP

if [ -z "$HA_IP" ]; then
    echo "Error: No IP provided"
    exit 1
fi

echo ""
echo "Step 1: Checking SSH connection..."
ssh root@${HA_IP} "echo 'Connected successfully'" || { echo "SSH failed!"; exit 1; }

echo ""
echo "Step 2: Checking current version on HA..."
ssh root@${HA_IP} "grep 'version:' /addons/newrelic-metrics/config.yaml"

echo ""
echo "Step 3: Force copying new files..."
rsync -av --progress \
    --exclude='.git' \
    --exclude='__pycache__' \
    newrelic-metrics/ root@${HA_IP}:/addons/newrelic-metrics/

echo ""
echo "Step 4: Verifying version on HA..."
ssh root@${HA_IP} "grep 'version:' /addons/newrelic-metrics/config.yaml"

echo ""
echo "Step 5: Checking for ha_token in config..."
ssh root@${HA_IP} "grep 'ha_token' /addons/newrelic-metrics/config.yaml" && echo "✓ ha_token found!" || echo "✗ ha_token missing!"

echo ""
echo "Done! Now in Home Assistant:"
echo "1. Go to the addon"
echo "2. Click Rebuild"
echo "3. Wait for build to complete"
echo "4. Check Info tab - should show version 1.0.1"
