#!/bin/bash

# Script to copy addon to Home Assistant for local testing
# Usage: ./copy-to-ha.sh [home-assistant-ip]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}New Relic Metrics Addon - Copy to Home Assistant${NC}"
echo "=================================================="
echo ""

# Get Home Assistant IP
if [ -z "$1" ]; then
    echo -e "${YELLOW}Please provide your Home Assistant IP address:${NC}"
    read -p "IP: " HA_IP
else
    HA_IP=$1
fi

# Validate IP
if [ -z "$HA_IP" ]; then
    echo -e "${RED}Error: No IP address provided${NC}"
    exit 1
fi

# Choose user
read -p "SSH user [root]: " HA_USER
HA_USER=${HA_USER:-root}

REMOTE_PATH="/addons/newrelic-metrics"

echo ""
echo -e "${GREEN}Configuration:${NC}"
echo "  Host: ${HA_USER}@${HA_IP}"
echo "  Path: ${REMOTE_PATH}"
echo ""

# Test SSH connection
echo -e "${YELLOW}Testing SSH connection...${NC}"
if ! ssh -o ConnectTimeout=5 ${HA_USER}@${HA_IP} "echo 'Connection successful'" > /dev/null 2>&1; then
    echo -e "${RED}Error: Cannot connect to ${HA_IP}${NC}"
    echo "Please check:"
    echo "  - SSH addon is installed and running"
    echo "  - IP address is correct"
    echo "  - SSH password/key is configured"
    exit 1
fi
echo -e "${GREEN}✓ Connection successful${NC}"
echo ""

# Create directory on remote
echo -e "${YELLOW}Creating directory on Home Assistant...${NC}"
ssh ${HA_USER}@${HA_IP} "mkdir -p ${REMOTE_PATH}"
echo -e "${GREEN}✓ Directory created${NC}"
echo ""

# Copy files using tar+scp (rsync not available on HA)
echo -e "${YELLOW}Copying addon files...${NC}"
tar czf /tmp/newrelic-metrics.tar.gz newrelic-metrics/
scp /tmp/newrelic-metrics.tar.gz ${HA_USER}@${HA_IP}:/tmp/
ssh ${HA_USER}@${HA_IP} "cd /tmp && tar xzf newrelic-metrics.tar.gz && rm -rf ${REMOTE_PATH}/* && mv newrelic-metrics/* ${REMOTE_PATH}/ && rm -rf newrelic-metrics newrelic-metrics.tar.gz"
rm /tmp/newrelic-metrics.tar.gz

echo ""
echo -e "${GREEN}✓ Files copied successfully!${NC}"
echo ""

# Show version
VERSION=$(ssh ${HA_USER}@${HA_IP} "grep 'version:' ${REMOTE_PATH}/config.yaml" | awk '{print $2}')
echo -e "${GREEN}Version copied: ${VERSION}${NC}"
echo ""

echo "Next steps:"
echo "1. Go to Home Assistant → Settings → Add-ons"
echo "2. Click ⋮ (three dots) → Reload"
echo "3. Look for 'New Relic Metrics' in Local add-ons"
echo "4. Click Install (or Rebuild if already installed)"
echo "5. Configure and start the addon"
echo ""
echo -e "${YELLOW}To update after making changes, run this script again${NC}"
