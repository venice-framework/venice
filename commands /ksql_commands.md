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
CREATE STREAM locations_stream
WITH (KAFKA_TOPIC='locations',
      PARTITIONS=3,
      VALUE_FORMAT='AVRO',
      KEY = 'bus_id');
```

- reminder STREAM = TOPIC + SCHEMA.
- partitions has to match the topic partitions I think.
- I got this error when trying to add it with partitions 1.

```
A Kafka topic with the name 'bus_locations' already exists, with different partition/replica configuration than required. KSQL expects 1 partitions (topic has 3), and 1 replication factor (topic has 1).
```

## Show STREAM

```sqls
SHOW STREAMS;
```

## set offset for a stream back to the start

```
SET 'auto.offset.reset' = 'earliest';
```

## Print the STREAM

```sql
SELECT * FROM bus_locations_stream EMIT CHANGES;
SELECT * FROM locations_stream EMIT CHANGES;


```

- you need to remember to do the EMIT CHANGES
- you might need to do this: select \* from purchases_stream emit changes;

## describe relationship between stream and topic

```
DESCRIBE EXTENDED just_buses2;
```

## Stream from select

CREATE STREAM just_buses_stream
WITH (VALUE_FORMAT='AVRO')
AS SELECT bus_id FROM locations_stream
PARTITION BY BUS_ID
EMIT CHANGES;

## Rekey a stream without a key

````sql
CREATE STREAM locations_with_lat_key
    WITH (KAFKA_TOPIC='locations_keyed_by_lat') AS
    SELECT *
    FROM  BUS_LOCATIONS_STREAM
    PARTITION BY lat;


-- then to query

SELECT * FROM locations_with_lat_key EMIT CHANGES;

```


## More complex query

SELECT ROWKEY, SUM(lng) AS total_lng
FROM locations_with_lat_key
GROUP BY ROWKEY
EMIT CHANGES;

CREATE new_stream
WITH (KAFKA_TOPIC='purchases', PARTITIONS=1, VALUE_FORMAT='AVRO');

select \* from purchases_stream emit changes;

-- reset the offset
SET 'auto.offset.reset'='earliest';

-- describes the relationship between a stream and a topic
describe extended purchases_stream;
````
