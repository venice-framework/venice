use cp-kafka-connect instead of cp-kafka-connect-base if you want JDBC Source Connector, JDBC Sink Connector, Elasticsearch Sink Connector,
and Amazon S3 Sink Connector bundled with the image
https://hub.docker.com/r/confluentinc/cp-kafka-connect
https://docs.confluent.io/current/connect/userguide.html#installing-kconnect-plugins

# Run the base image
docker run -it confluentinc/cp-kafka-connect-base:5.3.3 --name connect /bin/bash

# Install influxdb connector
confluent-hub install confluentinc/kafka-connect-influxdb:1.1.2
2, y, y, y

# Commit the changes to the container
docker commit 

# Create connect directory
## Create config file
## Create dockerfile

TODO: cleanup step: dynamically insert schema.registry.url based on an environment variable that you set in docker-compose.yml 