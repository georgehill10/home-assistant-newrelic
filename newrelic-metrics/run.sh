#!/usr/bin/with-contenv bashio

bashio::log.info "Starting New Relic Metrics addon..."

# Run the Python script
python3 /newrelic_sensor.py
