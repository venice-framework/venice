<!-- curl -X "POST" "http://localhost:18083/connectors/" \
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

}' -->

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

curl -X PUT http://kafka-connect:8083/connectors/sink-jdbc-mysql-01/config \
 -H "Content-Type: application/json" -d '{
"connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
"connection.url": "jdbc:mysql://mysql:3306/buses",
"topics": "bus_locations_stream",
"connection.user": "venice_user",
"connection.password": "venice",
"auto.create": true,
"auto.evolve": true,
"insert.mode": "upsert"
}'
