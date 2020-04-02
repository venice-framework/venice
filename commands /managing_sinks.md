## Steps to get the sink to work

- run docker-compose up
- wait for everything to be up and the producer is producing
  - the easiest way for me to test this has been to log onto ksql check there. COmmands below

```
from local machine
docker-compose exec ksqldb-cli  ksql http://primary-ksqldb-server:8088

in ksql
SHOW TOPICS
print topic_name;
```

- if you are getting a stream of data from the producer then it is working and you can try to create a sink by sending a POST / PUT request to http://localhost:8083/connectors

  - Sink requests are at the end of this document

- You can check kafka-connect and postgres to see if it worked.
  - to connect to our existing postgres set up you would run:

```
docker exec -it venice-python_postgres_1 psql --username=venice_user --dbname=buses
```

- then when connected you can check with these commands:

```sql
 \dt   --  this will show you if table is created
SELECT COUNT(*) FROM table_name; --> will tell you how many records there are. If you run that every couple of seconds you'll see new records are being added
SELECT * FROM table_name;  --> will give you the actual data.
```

- To check on kafka-connect you need

```
curl localhost:8083/connectors
```

## Full list of config that is sent along with each request

Posting this here because there might be some that we want to tweak.

- delete.enabled
- table.name.format - currently tables created are based off topic names
- insert.mode - I think we will definitly want a connector that does upsert, so we will have to come back and figure that out. IF you set upsert then you need to select primary key which means you need to look at these settings.
  - pk.fields
  - pk.mode

```
  auto.create = true
  auto.evolve = true
  batch.size = 3000
  connection.password = [hidden]
  connection.url = jdbc:postgresql://postgres:5432/buses
  connection.user = venice_user
  db.timezone = UTC
  delete.enabled = false
  dialect.name =
  fields.whitelist = []
  insert.mode = insert
  max.retries = 10
  pk.fields = []
  pk.mode = none
  quote.sql.identifiers = ALWAYS
  retry.backoff.ms = 3000
  table.name.format = ${topic}
```

## Sink Requests

- Anything in CAPS needs to be replaced.
  - SINK_NAME
  - DATABASE_NAME
  - TOPIC_NAME

### Sinking a topic created from python

- This will work without any key/value converters because AVRO is the default and we created key/value both in avro.
- If we change the producer so that the key is not in avro then we will have to update this.

```json
curl -X POST http://localhost:8083/connectors -H "Content-Type: application/json" -d '{
"name": "CONNECTOR_NAME",
"config": {
"connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
"connection.url": "jdbc:postgresql://postgres:5432/DATABASE_NAME",
"connection.user": "venice_user",
"connection.password": "venice",
"topics": "TOPIC_NAME",
"auto.create":"true",
"auto.evolve":"true",
"insert.mode": "insert"
}
}'
```

## Creating a sink from a KSQL STREAM as select

- The only difference here is that we've had to add a key.converter config.
- ksql does not use avro to deserialize keys. At all. This means if you create a STREAM AS SELECT (basically a stream from another stream) then the key will be a string.
- This means you need to add the key.converter here.

```
curl -X POST http://localhost:8083/connectors -H "Content-Type: application/json" -d '{
"name": "CONNECTOR_NAME",
"config": {
"connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
"connection.url": "jdbc:postgresql://postgres:5432/DATABASE_NAME",
"connection.user": "venice_user",
"connection.password": "venice",
"key.converter": "org.apache.kafka.connect.storage.StringConverter",
"topics": "TOPIC_NAME",
"auto.create":"true",
"auto.evolve":"true",
"insert.mode": "insert"
}
}'
```

## MySQL

Keeping this here for now.

### mysql command to creat the sink

```json
curl -X POST http://localhost:8083/connectors -H "Content-Type: application/json" -d '{
"name": "CONNECTOR_NAME",
"config": {
"connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
"connection.url": "jdbc:mysql://mysql:3306/DATABASE_NAME",
"connection.user": "venice_user",
"connection.password": "venice",
"topics": "TOPIC_NAME",
"auto.create":"true",
"auto.evolve":"true",
"insert.mode": "insert"
}
}'
```

## Actual test sinks as of April 2nd

```json
curl -X POST http://localhost:8083/connectors -H "Content-Type: application/json" -d '{
"name": "bus_locations",
"config": {
"connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
"connection.url": "jdbc:postgresql://postgres:5432/buses",
"connection.user": "venice_user",
"connection.password": "venice",
"topics": "bus_locations",
"auto.create":"true",
"auto.evolve":"true",
"insert.mode": "insert"
}
}'
```
