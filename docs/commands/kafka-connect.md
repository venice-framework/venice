https://docs.confluent.io/3.2.0/connect/managing.html

## View connectors

curl kafka-connect:8083/connectors

## Getting tasks for a connector

replace postgres-sink-1 with your connector name
curl kafka-connect:8083/connectors/sink-jdbc-mysql-01/tasks | jq

## Restart connector task

curl -s -X PUT host:port/connectors/postgres-sink-1/resume

### Delete a connector

curl -X DELETE http://kafka-connect:8083/connectors/CONNECTOR_NAME
curl -X DELETE http://kafka-connect:8083/connectors/bus_locations

## TODO: Combining with Melissa's notes from connectors course
