TIP: Set entrypoint as follows in the dockerfile of a container if you're having trouble getting it to stay up for debugging

ENTRYPOINT ["tail", "-f", "/dev/null"]

Run docker command like the following to run an interactive bash shell within the container.

docker exec -it confluent_producer_1 /bin/bash

# Check connnections to hosts
ping -c 3 amazon.com
ping -c 3 schema-registry.confluent_kafka

# Check connections to specific ports
nc -vz broker.confluent_kafka 29092
nc -vz schema-registry.confluent_kafka 28081 