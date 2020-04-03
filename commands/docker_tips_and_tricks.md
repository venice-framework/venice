https://rmoff.net/2018/12/15/docker-tips-and-tricks-with-ksql-and-kafka/

# Which command will the container run upon startup?

```
docker inspect --format='{{.Config.Entrypoint}}' confluentinc/cp-ksql-server:5.0.1
docker inspect --format='{{.Config.Cmd}}' confluentinc/cp-ksql-server:5.0.1
```

# How to make a container do some things before starting up in its usual way
1. Figure out what command it usually runs upon startup (see above for checking the ENTRYPOINT and CMD of an image)

2. Do something like the following in docker-compose.yml. In this example, `/etc/confluent/docker/run` is the default startup command.
The | tells YAML that the lines following it are all part of the same command. It allows you to pass multiple arguments to `/bin/bash` without putting them all on the same line. 

```
ksql-server:
  image: confluentinc/cp-ksql-server:5.0.1
  depends_on:
    - kafka
  environment:
    KSQL_BOOTSTRAP_SERVERS: kafka:29092
    KSQL_LISTENERS: http://0.0.0.0:8088
  command: 
    - /bin/bash
    - -c 
    - |
      mkdir -p /data/maxmind
      cd /data/maxmind
      curl https://geolite.maxmind.com/download/geoip/database/GeoLite2-City.tar.gz | tar xz 
      /etc/confluent/docker/run 
```

## Install a Kafka Plugin automatically
```
kafka-connect:
  image: confluentinc/cp-kafka-connect:5.1.2
  environment:
    CONNECT_REST_PORT: 8083
    CONNECT_REST_ADVERTISED_HOST_NAME: "kafka-connect"
    CONNECT_PLUGIN_PATH: '/usr/share/java,/usr/share/confluent-hub-components'
    […]
  volumes:
    - $PWD/scripts:/scripts
  command: 
    - bash 
    - -c 
    - |
      confluent-hub install --no-prompt neo4j/kafka-connect-neo4j:1.0.0
      /etc/confluent/docker/run
```
Note that you must also set CONNECT_PLUGIN_PATH to include the path into which the plugin is being installed, otherwise it won’t be picked up by Kafka Connect.

## Deploy a Kafka Connector automatically
```
kafka-connect:
  image: confluentinc/cp-kafka-connect:5.1.2
  environment:
    CONNECT_REST_PORT: 18083
    CONNECT_REST_ADVERTISED_HOST_NAME: "kafka-connect"
    […]
  volumes:
    - $PWD/scripts:/scripts
  command: 
    - bash 
    - -c 
    - |
      /etc/confluent/docker/run & 
      echo "Waiting for Kafka Connect to start listening on kafka-connect ⏳"
      while [ $$(curl -s -o /dev/null -w %{http_code} http://kafka-connect:8083/connectors) -eq 000 ] ; do 
        echo -e $$(date) " Kafka Connect listener HTTP state: " $$(curl -s -o /dev/null -w %{http_code} http://kafka-connect:8083/connectors) " (waiting for 200)"
        sleep 5 
      done
      nc -vz kafka-connect 8083
      echo -e "\n--\n+> Creating Kafka Connect Elasticsearch sink"
      /scripts/create-es-sink.sh 
      sleep infinity
```

# Wait for an HTTP endpoint to be available before doing something

```
echo -e "\n\nWaiting for KSQL to be available before launching CLI\n"
while [ $(curl -s -o /dev/null -w %{http_code} http://ksql-server:8088/) -eq 000 ]
do 
  echo -e $(date) "KSQL Server HTTP state: " $(curl -s -o /dev/null -w %{http_code} http://ksql-server:8088/) " (waiting for 200)"
  sleep 5
done
```

`echo -e "\n\nWaiting for KSQL to be available before launching CLI\n"`
`echo` displays a line of text
`-e` enables interpretation of backslash escapes, so `\n` would be interpreted as a new line

`while [ $(curl -s -o /dev/null -w %{http_code} http://ksql-server:8088/) -eq 000 ]`
`-s`: silent; don't show progress meter or error messages, only the output
`-o /dev/null`: write output to /dev/null (i.e., trash it) instead of to stdout
`-w %{http_code}`: write out http_code (code of the last retrieved HTTP(s) of FTP(s) transfer)

`$(curl -s -o /dev/null -w %{http_code} http://ksql-server:8088/)`
returns the http code of sending a GET request to http://ksql-server:8088
`-eq` inside of single braces does arithmetic comparisons in bash scripting.
`-eq 000` would compare the code to 000. You could also use 0 but Robin Moffat does it this way, probably so it would look more like an HTTP code.

