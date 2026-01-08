# Local Development Guide

This guide will help you test the New Relic Metrics addon locally before committing to git.

## Method 1: Test in Home Assistant (Recommended)

### For Home Assistant OS or Supervised

1. **Find your addons directory:**
   - SSH into your Home Assistant instance
   - The addons directory is typically at: `/addons/` or `/usr/share/hassio/addons/local/`

2. **Copy the addon:**
   ```bash
   # From your development machine
   scp -r newrelic-metrics root@YOUR_HA_IP:/addons/local/
   ```

   Or if you have direct access:
   ```bash
   cp -r newrelic-metrics /path/to/homeassistant/addons/local/
   ```

3. **Reload addons:**
   - In Home Assistant: Supervisor → Add-on Store → ⋮ → Reload

4. **Install and configure:**
   - Find "New Relic Metrics" in the local addons section
   - Install, configure, and start it

### For Home Assistant Container

If you're running Home Assistant in Docker, you'll need to use Method 2 or 3 below.

## Method 2: Test with Docker (No Home Assistant needed)

This method tests the addon container independently.

### Prerequisites

- Docker installed
- New Relic API key and account ID

### Steps

1. **Create a test configuration:**
   ```bash
   mkdir -p test-data
   cat > test-data/options.json << 'EOF'
   {
     "api_key": "YOUR_NEWRELIC_API_KEY",
     "account_id": "YOUR_ACCOUNT_ID",
     "update_interval": 60,
     "queries": [
       {
         "name": "test_metric",
         "nrql": "SELECT count(*) FROM Transaction SINCE 5 minutes ago",
         "icon": "mdi:chart-line"
       }
     ]
   }
   EOF
   ```

2. **Build the Docker image:**
   ```bash
   cd newrelic-metrics
   docker build --build-arg BUILD_FROM="ghcr.io/home-assistant/amd64-base:3.19" -t newrelic-metrics-test .
   ```

3. **Run the container:**
   ```bash
   docker run --rm \
     -v $(pwd)/../test-data:/data \
     -e SUPERVISOR_TOKEN="test-token" \
     newrelic-metrics-test
   ```

   **Note:** This will test the New Relic API connection but won't actually update Home Assistant sensors (since there's no HA instance).

## Method 3: Test Python Script Directly (Fastest)

This is the quickest way to test the core logic.

### Prerequisites

- Python 3.11+
- `requests` library

### Steps

1. **Install dependencies:**
   ```bash
   pip3 install requests
   ```

2. **Create a test configuration:**
   ```bash
   mkdir -p test-data
   cat > test-data/options.json << 'EOF'
   {
     "api_key": "YOUR_NEWRELIC_API_KEY",
     "account_id": "YOUR_ACCOUNT_ID",
     "update_interval": 30,
     "queries": [
       {
         "name": "test_metric",
         "nrql": "SELECT count(*) FROM Transaction SINCE 5 minutes ago",
         "icon": "mdi:chart-line"
       }
     ]
   }
   EOF
   ```

3. **Run the script with mock mode:**
   I'll create a development version of the script that can run standalone.

Let me create that for you...
