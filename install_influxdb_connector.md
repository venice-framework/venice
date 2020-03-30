
# Install
https://www.confluent.io/hub/confluentinc/kafka-connect-influxdb

`confluent-hub install confluentinc/kafka-connect-influxdb:1.1.2`

I don't know whether 1 or 2 is a better choice. I just picked 1.

```
root@connect:/etc/confluent-hub-client# confluent-hub install confluentinc/kafka-connect-influxdb:1.1.2
The component can be installed in any of the following Confluent Platform installations: 
  1. / (installed rpm/deb package) 
  2. / (where this tool is installed) 
Choose one of these to continue the installation (1-2): 2
Do you want to install this into /usr/share/confluent-hub-components? (yN) y

 
Component's license: 
Confluent Software Evaluation License 
https://www.confluent.io/software-evaluation-license 
I agree to the software license agreement (yN) y

Downloading component Kafka Connect InfluxDB 1.1.2, provided by Confluent, Inc. from Confluent Hub and installing into /usr/share/confluent-hub-components 
Detected Worker's configs: 
  1. Standard: /etc/kafka/connect-distributed.properties 
  2. Standard: /etc/kafka/connect-standalone.properties 
  3. Standard: /etc/schema-registry/connect-avro-distributed.properties 
  4. Standard: /etc/schema-registry/connect-avro-standalone.properties 
  5. Used by Connect process with PID : /etc/kafka-connect/kafka-connect.properties 
Do you want to update all detected configs? (yN) y

Adding installation directory to plugin path in the following files: 
  /etc/kafka/connect-distributed.properties 
  /etc/kafka/connect-standalone.properties 
  /etc/schema-registry/connect-avro-distributed.properties 
  /etc/schema-registry/connect-avro-standalone.properties 
  /etc/kafka-connect/kafka-connect.properties 
 
Completed 
```

# Configure
Standalone workers:
https://docs.confluent.io/current/connect/kafka-connect-influxdb/influx-db-sink-connector/index.html#property-based-example
Distributed workers: scroll down on page at the link above

```
name=InfluxDBSourceConnector
connector.class=io.confluent.influxdb.source.InfluxdbSourceConnector
tasks.max=1
topics=bus.locations
influxdb.url=http://localhost:8086
influxdb.db=testdb
mode=timestamp
value.converter=org.apache.kafka.connect.avro.AvroConverter
value.converter.schema.registry.url="http://schema-registry.confluent_kafka:28081"
```

According to the output from above, we should look in `/usr/share/confluent-hub-components` for the influxdb connector component.
The config file is located at `/usr/share/confluent-hub-components/confluentinc-kafka-connect-influxdb/etc/influxdb-source-connector.properties`