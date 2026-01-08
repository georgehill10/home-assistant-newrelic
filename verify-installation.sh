#!/bin/bash

# Verify addon files on Home Assistant

if [ -z "$1" ]; then
    echo "Usage: ./verify-installation.sh YOUR_HA_IP"
    exit 1
fi

HA_IP=$1
HA_USER=${2:-root}

echo "Checking addon files on Home Assistant..."
echo "==========================================="
echo ""

echo "1. Checking if directory exists:"
ssh ${HA_USER}@${HA_IP} "ls -la /addons/newrelic-metrics/" || echo "Directory not found!"
echo ""

echo "2. Checking config.yaml on Home Assistant:"
ssh ${HA_USER}@${HA_IP} "cat /addons/newrelic-metrics/config.yaml"
echo ""

echo "3. Checking for ha_token in config.yaml:"
ssh ${HA_USER}@${HA_IP} "grep -n 'ha_token' /addons/newrelic-metrics/config.yaml" || echo "ha_token NOT found in config!"
echo ""

echo "4. Checking file modification times:"
ssh ${HA_USER}@${HA_IP} "ls -lh /addons/newrelic-metrics/config.yaml"
echo ""
