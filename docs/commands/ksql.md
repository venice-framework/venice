## Connect to the ksqlCLI with our current docker set up

```
docker run --rm --name ksql-cli -it --network=venice-python_default confluentinc/cp-ksql-cli:5.4.1 http://ksql-server:8088
```

## Link to documentation

https://docs.ksqldb.io/en/latest/developer-guide/syntax-reference/

There is subsection on statements that work for ksql

## Show / print topics

```sql
SHOW TOPICS;
```

```sql
PRINT bus_locations FROM BEGINNING;  -- this will print beginnign and then follow
PRINT bus_locations; -- this will follow new input
```

## Create stream

- Stream names are case sensitive.
- so you can have a "locations" stream and a "LOCATIONS" stream.
- If you don't put the name in quotes then the stream will get created in ALL CAPS.
- So you either have to remember that or put quotes around them.
- If you are creating a STREAM that creates a topic e.g STREAM AS SELECT this is critical as the stream name and topic name may end up being different.

```sql
CREATE STREAM test
WITH (KAFKA_TOPIC='bus_locations',
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

## Show STREAMS that have been created

```sqls
SHOW STREAMS;
```

## set offset for a stream back to the start

```
SET 'auto.offset.reset' = 'earliest';
```

- This is important to do if you are creating a new stream.
- It applies to the "session".
- What it does it make the new stream read everything from the start of the topic.

## Print the stream

```sql
SELECT * FROM bus_locations_stream EMIT CHANGES;
SELECT * FROM locations_stream EMIT CHANGES;

```

- you need to remember to do the EMIT CHANGES

## describe relationship between stream and topic

```
DESCRIBE EXTENDED just_buses;
```

## Stream from select

```sql
CREATE STREAM just_buses_stream
WITH (VALUE_FORMAT='AVRO')
AS SELECT bus_id FROM locations_stream
PARTITION BY BUS_ID
EMIT CHANGES;
```

- You can do a step before this and just run the SELECT statement. - basically what we are doing is turning a select statement into a new stream (aka a new topic with a new schema)
  Making this AVRO format registeres the new schema with the schema registry
- PARTITION_BY - sets the key for this topic as the bus_id.
