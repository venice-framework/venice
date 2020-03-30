Note: Use cp-kafka-connect instead of cp-kafka-connect-base if you want JDBC Source Connector, JDBC Sink Connector, Elasticsearch Sink Connector,
and Amazon S3 Sink Connector bundled with the image
https://hub.docker.com/r/confluentinc/cp-kafka-connect
https://docs.confluent.io/current/connect/userguide.html#installing-kconnect-plugins

# Run the base image from docker-compose
Put this in docker-compose file under the "connect" service.
I think it's easier to run from docker-compose because the base image relies on communicating with the broker. The modified image will also depend on the schema-registry.

image: confluentinc/cp-kafka-connect-base:5.3.3

# Open bash shell and install influxdb connector in the container
docker exec -it connect /bin/bash
confluent-hub install confluentinc/kafka-connect-influxdb:1.1.2
2, y, y, y
CTRL+D to exit bash shell

# Commit the changes to the container
docker commit  -a "Nancy Trinh" -m "Installed influxdb connector" connect nantrinh/influxdb-connector 

# Create connector directory
Create config file.
Create Dockerfile.
