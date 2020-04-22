## How to set up postgres sink and check if it is working 
- Run `docker-compose up`
- Wait for everything to be up and the producer is producing; can use ksql to check
  - `venice ksql` to run ksql command line interface
  - `SHOW TOPICS;`
  - `PRINT bus_locations FROM BEGINNING;` to print all data from the beginning
  - `PRINT bus_locations` to follow new events
- If you are getting a stream of data from the producer then start a connector 
  - This config assumes `postgres` is the name of the postgres host, `5432` is the postgres port, and `buses` is the postgres database)
    If you are using a string for the key, you can set `"key.converter": "org.apache.kafka.connect.storage.StringConverter"`
    If you are using upsert, you can use `"insert.mode': "upsert"` and `"pk.mode": "record_key"` (see the confluent docs for other options for setting primary key)
    ```json
    curl -X POST http://localhost:8083/connectors -H "Content-Type: application/json" -d '{
    "name": "postgres_buses",
    "config": {
    "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
    "connection.url": "jdbc:postgresql://postgres:5432/buses",
    "connection.user": "venice_user",
    "connection.password": "venice",
    "key.converter": "io.confluent.connect.avro.AvroConverter",
    "value.converter": "io.confluent.connect.avro.AvroConverter",
    "topics": "bus_locations",
    "auto.create":"true",
    "auto.evolve":"true",
    "insert.mode": "insert"
    }
    }'
    ```
  - Connect to the postgres database and check if the table is populating
    - `docker exec -it postgres psql --username=venice_user --dbname=buses`
    - `\dt` to see if the table has been created
    - `SELECT * FROM bus_locations LIMIT 10;` to view the first ten rows
    - `SELECT COUNT(*) FROM bus_locations;` to view a count of how many records are in the table
    - You can run the select statement periodically to see if new records have been added.