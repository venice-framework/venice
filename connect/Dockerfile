# use cp-kafka-connect instead of cp-kafka-connect-base if you want JDBC Source Connector, JDBC Sink Connector, Elasticsearch Sink Connector,
# and Amazon S3 Sink Connector bundled with the image
# https://hub.docker.com/r/confluentinc/cp-kafka-connect
# https://docs.confluent.io/current/connect/userguide.html#installing-kconnect-plugins
FROM confluentinc/cp-kafka-connect-base:5.3.3
RUN confluent-hub install confluentinc/kafka-connect-influxdb:1.1.2
