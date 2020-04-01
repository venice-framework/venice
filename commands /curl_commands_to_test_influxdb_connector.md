# Is kafka connect running?
Enter a container on the network, for example the container responsible for starting a connector.

`docker exec -it venice-python_influxdb-connector-initializer_1 /bin/bash`

`curl http://connect:8083 -w "\n"`

should return something like:

`{"version":"5.3.3-ccs","commit":"b645a14492f6a68c","kafka_cluster_id":"LSkaoqGjQtafv9YSuDQKyA"}`

NOTE: you may want to install jq for prettier output
`apt-get update && apt-get install jq`

# What connectors are available?

`curl http://connect:8083/connectors -w "\n"`

Should return `[]` if you haven't started any connectors yet.

# Which plugins are available?
If using the nantrinh/influxdb-connector image, influxdb sink and source connectors should be displayed as well.

`curl http://connect:8083/connector-plugins | jq .`

```

[
  {
    "class": "io.confluent.influxdb.InfluxDBSinkConnector",
    "type": "sink",
    "version": "1.1.2"
  },
  {
    "class": "io.confluent.influxdb.source.InfluxdbSourceConnector",
    "type": "source",
    "version": "1.1.2"
  },
  {
    "class": "org.apache.kafka.connect.file.FileStreamSinkConnector",
    "type": "sink",
    "version": "5.4.1-ccs"
  },
  {
    "class": "org.apache.kafka.connect.file.FileStreamSourceConnector",
    "type": "source",
    "version": "5.4.1-ccs"
  },
  {
    "class": "org.apache.kafka.connect.mirror.MirrorCheckpointConnector",
    "type": "source",
    "version": "1"
  },
  {
    "class": "org.apache.kafka.connect.mirror.MirrorHeartbeatConnector",
    "type": "source",
    "version": "1"
  },
  {
    "class": "org.apache.kafka.connect.mirror.MirrorSourceConnector",
    "type": "source",
    "version": "1"
  }
]

```

# Start the influxdb-sink-connector
https://docs.confluent.io/current/connect/kafka-connect-influxdb/influx-db-sink-connector/index.html#rest-based-example

---
## On Environment Variables

These environment variables should be set if you're inside the container responsible for starting a connector:
CONNECT_URL, SCHEMA_REGISTRY_URL, INFLUXDB_URL, INFLUXDB_DB, TOPIC_NAME 

You can use `printenv` to check what values are set for those variables.

To create an environment variable:
```
MY_VAR='some_value'
export MY_VAR
```
Check that it was set:
`printenv MY_VAR`

---

## Start the connector

Note on cURL syntax: If you start the data with the letter @, the rest should be a file name to read the data from, or - if you want curl to read the data from stdin. Multiple files can also be specified.

```
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
```


Response:
```
{"name":"InfluxDBSinkConnector","config":{"connector.class":"io.confluent.influxdb.InfluxDBSinkConnector","tasks.max":"1","topics":"bus_locations","influxdb.url":"http://influxdb:8086","influxdb.db":"septaDB","measurement.name.format":"","value.converter":"io.confluent.connect.avro.AvroConverter","value.converter.schema.registry.url":"http://schema-registry:8081","name":"InfluxDBSinkConnector"},"tasks":[],"type":"sink"}
```

# Check status
curl http://connect:8083/connectors?expand=info&expand=status

curl -s -X PUT http://connect:8083/admin/loggers/io.confluent.influxdb \
    -H "Content-Type:application/json" \
    -d '{"level": "TRACE"}'

# Look inside influxdb to see if the table is being populated
`docker exec -it influxdb /bin/bash`

Log in to the influxDB shell:
`influx`

Output should look like:
```
Connected to http://localhost:8086 version 1.7.10
InfluxDB shell version: 1.7.10
```

Run the following queries to verify the results:
```
USE septaDB;
SELECT * FROM bus_locations ORDER BY desc LIMIT 5;
```