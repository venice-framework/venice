## Connect to the ksqlCLI with our current docker set up

docker-compose exec ksqldb-cli ksql http://primary-ksqldb-server:8088

## Show / print topics

```sql
SHOW TOPICS;
```

```sql
PRINT bus_locations FROM BEGINNING;  -- this will print beginnign and then follow
PRINT bus_locations; -- this will follow new input
```

## Create stream

```sql
CREATE STREAM bus_locations_stream
WITH (KAFKA_TOPIC='bus_locations', PARTITIONS=3, VALUE_FORMAT='AVRO');
```

- reminder STREAM = TOPIC + SCHEMA.
- partitions has to match the topic partitions I think.
- I got this error when trying to add it with partitions 1.

```
A Kafka topic with the name 'bus_locations' already exists, with different partition/replica configuration than required. KSQL expects 1 partitions (topic has 3), and 1 replication factor (topic has 1).
```

## Show STREAM

```sql
SHOW STREAMS;
```

## Print the STREAM

```sql
SELECT * FROM bus_locations_stream EMIT CHANGES;
```

- you need to remember to do the EMIT CHANGES
- you might need to do this: select \* from purchases_stream emit changes;

## describe relationship between stream and topic

```
DESCRIBE EXTENDED BUS_LOCATIONS;
```

## More complex query

SELECT ROWKEY, SUM(LAT) AS total_lat
FROM bus_locations_stream
GROUP BY ROWKEY
EMIT CHANGES;

CREATE new_stream
WITH (KAFKA_TOPIC='purchases', PARTITIONS=1, VALUE_FORMAT='AVRO');

select \* from purchases_stream emit changes;

-- reset the offset
SET 'auto.offset.reset'='earliest';

-- describes the relationship between a stream and a topic
describe extended purchases_stream;
