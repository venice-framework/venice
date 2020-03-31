use cp-kafka-connect instead of cp-kafka-connect-base if you want JDBC Source Connector, JDBC Sink Connector, Elasticsearch Sink Connector,
and Amazon S3 Sink Connector bundled with the image
https://hub.docker.com/r/confluentinc/cp-kafka-connect
https://docs.confluent.io/current/connect/userguide.html#installing-kconnect-plugins

# Run the base image
in docker-compose, because it depends on the broker

# Open a bash shell in the connector
docker exec -it connector /bin/bash

# Install influxdb connector
confluent-hub install confluentinc/kafka-connect-influxdb:1.1.2
2, y, y, y
CTRL+D to exit

# Commit the modified image
docker commit -a "Nancy Trinh" -m "Install influxdb connector" connector nantrinh/influxdb-connector:latest

# Push to repo (OPTIONAL)
docker push nantrinh/influxdb-connector:latest