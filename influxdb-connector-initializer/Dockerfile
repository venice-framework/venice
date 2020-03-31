FROM ubuntu:18.04
RUN apt-get update && apt-get install curl -y
COPY influxdb-sink-connector.json /app/influxdb-sink-connector.json 
COPY post_to_connector.sh /usr/local/bin/docker-entrypoint.sh 
RUN ["chmod", "+x", "/usr/local/bin/docker-entrypoint.sh"]
ENTRYPOINT ["docker-entrypoint.sh"]
