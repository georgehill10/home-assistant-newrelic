#!/usr/bin/env python3
"""New Relic Metrics integration for Home Assistant."""
import json
import logging
import os
import sys
import time
from typing import Any, Dict, List, Optional

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

NERDGRAPH_URL = "https://api.newrelic.com/graphql"
# Try multiple possible Home Assistant API endpoints
HOMEASSISTANT_URLS = [
    "http://homeassistant:8123/api",
    "http://supervisor/core/api",
    "http://localhost:8123/api",
]


class NewRelicClient:
    """Client for New Relic NerdGraph API."""

    def __init__(self, api_key: str, account_id: str):
        """Initialize the New Relic client."""
        self.api_key = api_key
        self.account_id = account_id
        self.headers = {
            "Content-Type": "application/json",
            "API-Key": self.api_key,
        }

    def query_nrql(self, nrql: str) -> Optional[Any]:
        """Execute a NRQL query using NerdGraph API."""
        graphql_query = """
        query($accountId: Int!, $nrql: Nrql!) {
          actor {
            account(id: $accountId) {
              nrql(query: $nrql) {
                results
              }
            }
          }
        }
        """

        payload = {
            "query": graphql_query,
            "variables": {
                "accountId": int(self.account_id),
                "nrql": nrql,
            },
        }

        try:
            response = requests.post(
                NERDGRAPH_URL,
                headers=self.headers,
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()

            if "errors" in data:
                logger.error(f"NerdGraph errors: {data['errors']}")
                return None

            results = data.get("data", {}).get("actor", {}).get("account", {}).get("nrql", {}).get("results", [])
            return results
        except requests.exceptions.RequestException as e:
            logger.error(f"Error querying New Relic: {e}")
            return None


class HomeAssistantAPI:
    """Client for Home Assistant API."""

    def __init__(self, ha_token: str):
        """Initialize the Home Assistant API client."""
        if not ha_token:
            logger.error("Home Assistant token not provided!")
        else:
            logger.info("Home Assistant token configured")

        self.headers = {
            "Authorization": f"Bearer {ha_token}",
            "Content-Type": "application/json",
        }

        # Find working HA URL
        self.base_url = self._find_working_url()

    def _find_working_url(self) -> str:
        """Find the working Home Assistant API URL."""
        for url in HOMEASSISTANT_URLS:
            try:
                logger.info(f"Testing Home Assistant API at {url}")
                response = requests.get(
                    f"{url}/",
                    headers=self.headers,
                    timeout=5,
                )
                if response.status_code in [200, 401]:  # 401 means auth is working but might need different endpoint
                    logger.info(f"✓ Using Home Assistant API at {url}")
                    return url
            except Exception as e:
                logger.debug(f"Cannot reach {url}: {e}")
                continue

        # Default to first one
        logger.warning(f"Could not verify HA API, using default: {HOMEASSISTANT_URLS[0]}")
        return HOMEASSISTANT_URLS[0]

    def update_sensor(
        self,
        entity_id: str,
        state: Any,
        attributes: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Update or create a sensor in Home Assistant."""
        url = f"{self.base_url}/states/{entity_id}"

        payload = {
            "state": str(state),
            "attributes": attributes or {},
        }

        try:
            logger.debug(f"Updating sensor {entity_id} at {url}")
            response = requests.post(
                url,
                headers=self.headers,
                json=payload,
                timeout=10,
            )
            response.raise_for_status()
            logger.info(f"Updated sensor {entity_id} with state: {state}")
            return True
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error updating sensor {entity_id}: {e}")
            logger.error(f"Response: {e.response.text if hasattr(e, 'response') else 'N/A'}")
            logger.error(f"URL: {url}")
            logger.error(f"Headers: {self.headers}")
            return False
        except requests.exceptions.RequestException as e:
            logger.error(f"Error updating Home Assistant sensor {entity_id}: {e}")
            return False


class NewRelicMetricsAddon:
    """Main addon class."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize the addon."""
        self.config = config
        self.nr_client = NewRelicClient(
            config["api_key"],
            config["account_id"],
        )
        self.ha_client = HomeAssistantAPI(config["ha_token"])
        self.update_interval = config.get("update_interval", 300)

    def process_query(self, query_config: Dict[str, Any]) -> None:
        """Process a single NRQL query and update Home Assistant."""
        name = query_config["name"]
        nrql = query_config["nrql"]
        value_field = query_config.get("value_field")
        decimal_places = query_config.get("decimal_places")
        unit_of_measurement = query_config.get("unit_of_measurement")
        icon = query_config.get("icon", "mdi:chart-line")

        logger.info(f"Processing query: {name}")
        logger.debug(f"NRQL: {nrql}")

        results = self.nr_client.query_nrql(nrql)

        if results is None:
            logger.warning(f"No results for query: {name}")
            return

        if not results:
            logger.warning(f"Empty results for query: {name}")
            return

        # Get the first result
        result = results[0]
        logger.info(f"Query result fields: {list(result.keys())}")

        # Extract the value
        state = None

        if value_field:
            # Use specific field if specified
            if value_field in result:
                state = result[value_field]
                logger.info(f"Extracted value from field '{value_field}': {state}")
            else:
                logger.warning(f"Field '{value_field}' not found in result. Available fields: {list(result.keys())}")
                logger.warning(f"Falling back to show all fields")
                # Fallback to showing all fields as JSON
                filtered_result = {k: v for k, v in result.items() if k not in ['beginTimeSeconds', 'endTimeSeconds', 'facet']}
                state = json.dumps(filtered_result)
                logger.info(f"Showing all fields as state: {state}")
        else:
            # No value_field specified - show all fields as JSON string in state
            filtered_result = {k: v for k, v in result.items() if k not in ['beginTimeSeconds', 'endTimeSeconds', 'facet']}
            state = json.dumps(filtered_result)
            logger.info(f"No value_field specified, showing all fields: {state}")

        if state is None:
            logger.warning(f"Could not extract value from result: {result}")
            return

        # Round to decimal places if specified and value is numeric
        if decimal_places is not None and isinstance(state, (int, float)):
            state = round(float(state), decimal_places)
            logger.info(f"Rounded to {decimal_places} decimal places: {state}")

        # Create entity ID from query name
        entity_id = f"sensor.newrelic_{name.lower().replace(' ', '_').replace('-', '_')}"

        # Prepare attributes
        attributes = {
            "friendly_name": f"New Relic: {name}",
            "icon": icon,
            "query": nrql,
            "account_id": self.config["account_id"],
        }

        if unit_of_measurement:
            attributes["unit_of_measurement"] = unit_of_measurement

        # Add all result fields as attributes
        for key, value in result.items():
            if key not in ['beginTimeSeconds', 'endTimeSeconds']:
                attributes[f"nr_{key}"] = value

        # Update the sensor
        self.ha_client.update_sensor(entity_id, state, attributes)

    def run(self) -> None:
        """Run the addon main loop."""
        logger.info("New Relic Metrics addon started")
        logger.info(f"Update interval: {self.update_interval} seconds")
        logger.info(f"Number of queries: {len(self.config['queries'])}")

        while True:
            try:
                for query in self.config["queries"]:
                    self.process_query(query)

                logger.info(f"Sleeping for {self.update_interval} seconds")
                time.sleep(self.update_interval)
            except KeyboardInterrupt:
                logger.info("Shutting down...")
                break
            except Exception as e:
                logger.error(f"Unexpected error: {e}", exc_info=True)
                time.sleep(60)  # Wait a minute before retrying


def load_config() -> Dict[str, Any]:
    """Load configuration from options.json."""
    config_path = "/data/options.json"

    if not os.path.exists(config_path):
        logger.error(f"Configuration file not found: {config_path}")
        sys.exit(1)

    with open(config_path, "r") as f:
        config = json.load(f)

    # Validate required fields
    if not config.get("api_key"):
        logger.error("New Relic API key not configured")
        sys.exit(1)

    if not config.get("account_id"):
        logger.error("New Relic account ID not configured")
        sys.exit(1)

    if not config.get("ha_token"):
        logger.error("Home Assistant token not configured")
        logger.error("Please create a long-lived access token in Home Assistant:")
        logger.error("  1. Go to your Profile (click your name in the sidebar)")
        logger.error("  2. Scroll to 'Long-Lived Access Tokens'")
        logger.error("  3. Click 'Create Token'")
        logger.error("  4. Copy the token and add it to the addon configuration")
        sys.exit(1)

    if not config.get("queries"):
        logger.error("No queries configured")
        sys.exit(1)

    return config


def main():
    """Main entry point."""
    config = load_config()
    addon = NewRelicMetricsAddon(config)
    addon.run()


if __name__ == "__main__":
    main()
