curl -X "POST" "http://localhost:18083/connectors/" \
 -H "Content-Type: application/json" \
 -d '{
"name": "postgres_buses",
"config": {
"connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
"connection.url": "jdbc:postgresql://postgres:5432/buses?user=venice_user&password=venice",
"auto.create":"true",
"auto.evolve":"true",
"topics": "bus_locations",
"key.converter": "org.apache.kafka.connect.storage.StringConverter",
"value.converter": "io.confluent.connect.avro.AvroConverter",
"insert.mode": "upsert"

}'
