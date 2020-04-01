#!/bin/bash
sleep 2m && \
echo \
"{
  \"name\" : \"InfluxDBSinkConnector\",
  \"config\" : {
    \"connector.class\" : \"io.confluent.influxdb.InfluxDBSinkConnector\",
    \"tasks.max\" : \"1\",
    \"topics\" : \"$TOPIC_NAME\",
    \"influxdb.url\" : \"$INFLUXDB_URL\",
    \"influxdb.db\" : \"$INFLUXDB_DB\",
    \"measurement.name.format\" : \"${topic}\",
    \"value.converter\": \"io.confluent.connect.avro.AvroConverter\",
    \"value.converter.schema.registry.url\": \"$SCHEMA_REGISTRY_URL\"
  }
}" | curl -X POST -d @- $CONNECT_URL/connectors -H "Content-Type: application/json" -w "\n"