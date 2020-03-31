# Is the connector running?
## Checking from localhost
curl http://localhost:8083

should return something like:

{"version":"5.3.3-ccs","commit":"b645a14492f6a68c","kafka_cluster_id":"LSkaoqGjQtafv9YSuDQKyA"}

# What connectors are available?
curl http://connector:8083/connectors

# Which plugins are available?
curl http://localhost:8083/connector-plugins

```
[
  {"class":"org.apache.kafka.connect.file.FileStreamSinkConnector","type":"sink","version":"5.4.1-ccs"},
  {"class":"org.apache.kafka.connect.file.FileStreamSourceConnector","type":"source","version":"5.4.1-ccs"},
  {"class":"org.apache.kafka.connect.mirror.MirrorCheckpointConnector","type":"source","version":"1"},
  {"class":"org.apache.kafka.connect.mirror.MirrorHeartbeatConnector","type":"source","version":"1"},
  {"class":"org.apache.kafka.connect.mirror.MirrorSourceConnector","type":"source","version":"1"}
]
```
# Create influxdb-sink-connector.json file
Example here: https://docs.confluent.io/current/connect/kafka-connect-influxdb/influx-db-sink-connector/index.html#rest-based-example

# Post the config to one of the kafka connect workers
curl -X POST -d @influxdb-sink-connector.json http://localhost:8083/connectors -H "Content-Type: application/json"

From cURL man pages: If you start the data with the letter @, the rest should be a file name to read the data from, or - if you want curl to read the data from stdin. Multiple files can also be specified.

Response should like this:
{
  "name":"InfluxDBSinkConnector",
  "config":{
    "connector.class":"io.confluent.influxdb.InfluxDBSinkConnector",
     "tasks.max":"1",
     "topics":"bus_locations",
     "influxdb.url":"http://influxdb:28086",
     "influxdb.db":"influxTestDB",
     "measurement.name.format":"${topic}",
     "value.converter":"io.confluent.connect.avro.AvroConverter",
     "value.converter.schema.registry.url":"http://schema-registry:28081",
     "name":"InfluxDBSinkConnector"
  },
  "tasks":[],
  "type":"sink"
}

# Look inside influxdb to see if the table is being populated
```
docker exec -it influxdb /bin/bash
```

Log in to the influxDB shell:
```
influx
```

Output should look like:
```
Connected to http://influxdb:8086 version 1.7.7
InfluxDB shell version: 1.7.7
```

Run the following queries to verify the results:
```
USE influxTestDB;
SELECT * FROM bus_locations ORDER BY desc LIMIT 5;
```