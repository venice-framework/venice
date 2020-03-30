# Look inside connector to see if the config file is in the right place and contains the right info 
docker exec -it connector /bin/bash
cd /usr/share/confluent-hub-components/confluentinc-kafka-connect-influxdb/etc/
cat influxdb-sink-connector.properties

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
Connected to http://influxdb.confluent_kafka:8086 version 1.7.7
InfluxDB shell version: 1.7.7
```

Run the following queries to verify the results:
```
USE influxTestDB;
SELECT * FROM bus_locations ORDER BY desc LIMIT 5;
```