https://docs.confluent.io/current/schema-registry/using.html
https://docs.confluent.io/current/schema-registry/schema_registry_tutorial.html

The schema url is http://schema-registry.confluent_kafka:28081

For slightly prettier output, add the --silent flag, and pipe the output to jq.
For example:
curl --silent -X GET http://localhost:8081/schemas/ids/1 | jq .

You may have to run

apt-get update && apt-get install jq

inside your container.

# Create a schema:

curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" --data '{"schema": "{\"type\":\"record\",\"name\":\"Payment\",\"namespace\":\"io.confluent.examples.clients.basicavro\",\"fields\":[{\"name\":\"id\",\"type\":\"string\"},{\"name\":\"amount\",\"type\":\"double\"}]}"}' http://schema-registry.confluent_kafka:28081/subjects/test-value/versions -w "\n"


You should see {"id": 1} returned, if this is the first schema you have registered.

# View all the subjects registered in the schema registry:
curl -X GET http://schema-registry.confluent_kafka:28081/subjects/ -w "\n"

# View the latest schema for the "test-value" subject in more detail:
curl -X GET http://schema-registry.confluent_kafka:28081/subjects/test-value/versions/latest -w "\n"

# View the schema with id 1 
curl -X GET http://schema-registry.confluent_kafka:28081/schemas/ids/1