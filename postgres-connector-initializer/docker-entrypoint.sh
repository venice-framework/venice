#!/bin/bash
sleep 3m && \
echo \
"{
  \"name\" : \"postgres_buses_upsert_bus_locations\",
  \"config\" : {
    \"connector.class\" : \"io.confluent.connect.jdbc.JdbcSinkConnector\",
     \"connection.url\": \"jdbc:postgresql://$POSTGRES_HOST:$POSTGRES_PORT/$POSTGRES_DB\",
     \"connection.user\": \"$POSTGRES_USER\",
     \"connection.password\": \"$POSTGRES_PASSWORD\",
     \"topics\": \"$TOPIC_NAME\",
     \"auto.create\":\"true\",
     \"auto.evolve\":\"true\",
     \"insert.mode\": \"upsert\",
     \"pk.mode\": \"record_key\"
  }
}" | curl -X POST -d @- $CONNECT_URL/connectors -H "Content-Type: application/json" -w "\n"