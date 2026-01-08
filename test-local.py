#!/usr/bin/env python3
"""
Local testing script for New Relic Metrics addon.
This allows you to test the New Relic API integration without Home Assistant.
"""
import json
import logging
import sys
from typing import Any, Dict, Optional

import requests

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

NERDGRAPH_URL = "https://api.newrelic.com/graphql"


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
            logger.info(f"Executing NRQL query: {nrql}")
            response = requests.post(
                NERDGRAPH_URL,
                headers=self.headers,
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()

            if "errors" in data:
                logger.error(f"NerdGraph errors: {json.dumps(data['errors'], indent=2)}")
                return None

            results = data.get("data", {}).get("actor", {}).get("account", {}).get("nrql", {}).get("results", [])
            logger.info(f"Query returned {len(results)} results")
            return results
        except requests.exceptions.RequestException as e:
            logger.error(f"Error querying New Relic: {e}")
            return None


def test_query(client: NewRelicClient, query_config: Dict[str, Any]) -> None:
    """Test a single NRQL query."""
    name = query_config["name"]
    nrql = query_config["nrql"]
    unit_of_measurement = query_config.get("unit_of_measurement")
    icon = query_config.get("icon", "mdi:chart-line")

    logger.info("=" * 80)
    logger.info(f"Testing query: {name}")
    logger.info(f"NRQL: {nrql}")
    logger.info("=" * 80)

    results = client.query_nrql(nrql)

    if results is None:
        logger.warning(f"❌ No results for query: {name}")
        return

    if not results:
        logger.warning(f"❌ Empty results for query: {name}")
        return

    # Get the first result
    result = results[0]
    logger.info(f"✓ Raw result: {json.dumps(result, indent=2)}")

    # Try to extract a numeric value from the result
    state = None
    for key in result:
        if key not in ['beginTimeSeconds', 'endTimeSeconds', 'facet']:
            state = result[key]
            break

    if state is None:
        logger.warning(f"❌ Could not extract value from result")
        return

    # Create entity ID from query name
    entity_id = f"sensor.newrelic_{name.lower().replace(' ', '_').replace('-', '_')}"

    # Prepare attributes
    attributes = {
        "friendly_name": f"New Relic: {name}",
        "icon": icon,
        "query": nrql,
    }

    if unit_of_measurement:
        attributes["unit_of_measurement"] = unit_of_measurement

    # Add all result fields as attributes
    for key, value in result.items():
        if key not in ['beginTimeSeconds', 'endTimeSeconds']:
            attributes[f"nr_{key}"] = value

    logger.info("✓ Sensor would be created:")
    logger.info(f"  Entity ID: {entity_id}")
    logger.info(f"  State: {state}")
    logger.info(f"  Attributes: {json.dumps(attributes, indent=4)}")
    logger.info("=" * 80)
    print()


def load_config(config_path: str = "test-data/options.json") -> Dict[str, Any]:
    """Load configuration from file."""
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {config_path}")
        logger.error("\nCreate a configuration file with:")
        logger.error(f"""
cat > {config_path} << 'EOF'
{{
  "api_key": "YOUR_NEWRELIC_API_KEY",
  "account_id": "YOUR_ACCOUNT_ID",
  "update_interval": 60,
  "queries": [
    {{
      "name": "test_metric",
      "nrql": "SELECT count(*) FROM Transaction SINCE 5 minutes ago",
      "icon": "mdi:chart-line"
    }}
  ]
}}
EOF
        """)
        sys.exit(1)

    # Validate required fields
    if not config.get("api_key"):
        logger.error("New Relic API key not configured")
        sys.exit(1)

    if not config.get("account_id"):
        logger.error("New Relic account ID not configured")
        sys.exit(1)

    if not config.get("queries"):
        logger.error("No queries configured")
        sys.exit(1)

    return config


def main():
    """Main entry point."""
    print("\n" + "=" * 80)
    print("New Relic Metrics Addon - Local Testing")
    print("=" * 80 + "\n")

    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    else:
        config_path = "test-data/options.json"

    config = load_config(config_path)

    logger.info(f"API Key: {config['api_key'][:15]}...")
    logger.info(f"Account ID: {config['account_id']}")
    logger.info(f"Number of queries: {len(config['queries'])}")
    print()

    client = NewRelicClient(config["api_key"], config["account_id"])

    for query in config["queries"]:
        test_query(client, query)

    print("=" * 80)
    print("✓ Testing complete!")
    print("=" * 80)
    print("\nIf all queries succeeded, your configuration is correct and ready to use.")
    print("Next steps:")
    print("  1. Copy newrelic-metrics/ to your Home Assistant addons directory")
    print("  2. Or commit to git and add the repository to Home Assistant")
    print()


if __name__ == "__main__":
    main()
