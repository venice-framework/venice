curl -X PUT http://localhost:8083/connectors/postgres-sink-1/config \
 -H "Content-Type: application/json" -d '{
"connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
"tasks.max": "1",
"connection.url": "jdbc:postgres://postgres:5432/buses",
"topics": "bus_locations",
"key.converter": "org.apache.kafka.connect.storage.StringConverter",
"value.converter": "io.confluent.connect.avro.AvroConverter",
"value.converter.schemas.enable": "true",
"connection.user": "venice_user",
"connection.password": "venice",
"auto.create": true,
"auto.evolve": true,
"insert.mode": "upsert",
"pk.mode": "record_key",
"pk.fields": "MESSAGE_KEY"
}'

curl -X PUT http://kafka-connect:8083/connectors/postgres-sink-1/config \
 -H "Content-Type: application/json" -d '{
"connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
"tasks.max": "1",
"connection.url": "jdbc:postgres://postgres:5432/buses",
"topics": "bus_locations",
"key.converter": "org.apache.kafka.connect.storage.StringConverter",
"value.converter": "io.confluent.connect.avro.AvroConverter",
"value.converter.schemas.enable": "true",
"connection.user": "venice_user",
"connection.password": "venice",
"auto.create": true,
"auto.evolve": true,
"insert.mode": "upsert",
"pk.mode": "record_key",
"pk.fields": "MESSAGE_KEY"
}'
