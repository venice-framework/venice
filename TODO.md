# definitely

## right now this is a manual step. how to automate? 

curl -X POST -d @influxdb-sink-connector.json http://connector:8083/connectors -H "Content-Type: application/json"

# maybe
should be able to define the topic you are working with in one place, and have it update multiple files (producer, consumer, influxdb config)