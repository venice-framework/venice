# Things that are new:

- mysql, postgres and connect images
- data folder that runs sql commands to create buses databases for both mysql and postgres
- a whole lot of configs for the ksql-db image which I added AFTER getting it work. Trying to fix some other things related to the key.
- I've tried to document them as much as possible

## outstanding issues

- I have an unmerged change to the producer that updates adds 1 to the key each time.
- I haven't gotten it to work properly so I haven't merged it.

## Steps to get the sink to work

- run docker-compose up
- wait for everything to be up and the producer is producing
  - the easiest way for me to test this has been to log onto ksql check there. COmmands below

```
from local machine
docker-compose exec ksqldb-cli  ksql http://primary-ksqldb-server:8088

in ksql
SHOW TOPICS
print bus_locations;
```

- if you are getting a stream of data from the producer then run one of the commands below

##3 postgres command to create the sink

```json
curl -X POST http://localhost:8083/connectors -H "Content-Type: application/json" -d '{
"name": "postgres_buses",
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

- connect to the database
  postgres

```
docker exec -it venice-python_postgres_1 psql --username=venice_user --dbname=buses

then when connected
\dt     -> this will show you if table is created
select count(*) from bus_locations; --> will tell you how many records there are. If you run that every couple of seconds you'll see new records are being added
select * from bus_locations;  --> will give you the actual data.


```

- success (hopefully).
  - the kafka-connect broker has decent logs if things don't work.

### mysql command to creat the sink

```json
curl -X POST http://localhost:8083/connectors -H "Content-Type: application/json" -d '{
"name": "mysql_buses",
"config": {
"connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
"connection.url": "jdbc:mysql://mysql:3306/buses",
"connection.user": "venice_user",
"connection.password": "venice",
"topics": "bus_locations",
"auto.create":"true",
"auto.evolve":"true",
"insert.mode": "insert"
}
}'
```
