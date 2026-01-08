# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-08

### Added
- Initial production release of New Relic Metrics addon
- Support for executing NRQL queries via New Relic NerdGraph API
- Automatic creation of Home Assistant sensors from query results
- Configurable update intervals (default: 5 minutes)
- Support for multiple queries per addon instance
- **value_field**: Extract specific field from multi-field query results
- **decimal_places**: Round numeric sensor values to specified precision
- Custom units of measurement for sensors
- Custom Material Design Icons for sensors
- Comprehensive error handling and logging
- Multi-architecture support (aarch64, amd64, armhf, armv7, i386)
- Home Assistant Long-Lived Access Token authentication

### Features
- Query any New Relic data source (APM, Infrastructure, Browser, Synthetics, Custom Events)
- Flexible field extraction: specify field name or auto-detect first field
- Show all query fields as JSON when no value_field specified
- All query result fields exposed as sensor attributes (prefixed with `nr_`)
- Query and account information stored as sensor attributes
- Automatic API endpoint detection for Home Assistant connectivity
- Detailed logging for debugging
- Example configurations for common use cases
- Comprehensive documentation and troubleshooting guides

### Technical Details
- Python 3-based integration using requests library
- NerdGraph GraphQL API for New Relic queries
- Home Assistant REST API for sensor updates
- Sequential query execution to avoid API rate limits
- Graceful error handling with detailed logging

[1.0.0]: https://github.com/georgehill10/home-assistant-newrelic/releases/tag/v1.0.0
