# Managing Kafka-Connect via HTTP

## documentation here

https://docs.confluent.io/3.2.0/connect/managing.html

## Useful ones

### Show current connectors

curl localhost:8083/connectors

### Delete a connector

curl -X DELETE http://localhost:8083/connectors/CONNECTOR_NAME

## TODO - Combining with Melissa's notes from connectors course
