# definitely
the config file for influxdb-connector is very brittle right now -- it has hardcoded urls for itself and schema registry. should dynamically insert based on environment variables that you set in docker-compose.yml 

remove the kafka network specification -- how does this change the network names?

# maybe
should be able to define the topic you are working with in one place, and have it update multiple files (producer, consumer, influxdb config)