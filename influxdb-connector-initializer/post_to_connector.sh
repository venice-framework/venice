#!/bin/bash
sleep 2m && curl -X POST -d @/app/influxdb-sink-connector.json ${CONNECTOR_URL}/connectors -H "Content-Type: application/json" && echo "I'm done"