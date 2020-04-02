One manual thing you seem to need to do is to make sure that the JDBC driver is downloaded and placed in the right folder for ANY kafka-connect container that is running.

If you have multiple in a cluster you need to do this in each.

If you look at the docker-compose.yml they had this command sequence at the end of the Kafka-Connect iamge

```
  command: # bust
      - bash
      - -c
      - |
        echo "Installing connector plugins"
        confluent-hub install --no-prompt confluentinc/kafka-connect-jdbc:5.4.1
        confluent-hub install --no-prompt jcustenborder/kafka-connect-spooldir:2.0.43
        #
        echo "Downloading JDBC driver"
        cd /usr/share/confluent-hub-components/confluentinc-kafka-connect-jdbc
        curl https://cdn.mysql.com/Downloads/Connector-J/mysql-connector-java-8.0.19.tar.gz | tar xz
        #

        # lets try add the postgres one here too

        curl https://jdbc.postgresql.org/download/postgresql-42.2.11.jar --output pg-jdbc-driver.jar
        echo "Launching Kafka Connect worker"
        /etc/confluent/docker/run &
        #
        sleep infinity
```

### Check location of where the JDBC should be

docker-compose logs kafka-connect | grep kafka-connect-jdbc | more

Can use this to get the localtion of the driver - its going to be something like:

usr/share/confluent-hub-components/confluentinc-kafka-connect-jdbc

### Make sure the JDBC driver is in that folder

- connect to kafka-connect container and then cd into that path you just copied
- The jar file for your connector MUST exist here. This is where connector plugins are loaded from.
- It applies to source/sink connectors.
- it doesn't matter how nested it is in that folder, but it should be there.
- The kafka-connect shifts with postgres, sqllite and a few others so I'm not sure why postgres isn't working by default
- mysql needs to be added.

### downlodaing files with curl

```
curl http://some.url --output some.file
```

That --output flag denotes the filename (some.file) of the downloaded URL (http://some.url)
