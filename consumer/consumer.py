from confluent_kafka import KafkaError
from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError

import os
import time

BROKER = os.environ['BROKER']
SCHEMA_REGISTRY_URL = os.environ['SCHEMA_REGISTRY_URL']
TOPIC_NAME = os.environ['TOPIC_NAME'] 

# sleep to give the schema-registry time to connect to kafka 
for i in range(120):
  print("I am sleeping for {} seconds".format(i))
  time.sleep(1)
print("I am done sleeping")

c = AvroConsumer({
    'bootstrap.servers': BROKER,
    'group.id': 'groupid',
    'schema.registry.url': SCHEMA_REGISTRY_URL})

c.subscribe([TOPIC_NAME])

while True:
    try:
        # block for 10s max waiting for message
        msg = c.poll(timeout=10)

    except SerializerError as e:
        # Report malformed record, discard results, continue polling
        print("Message deserialization failed for {}: {}".format(msg, e))
        break

    # There were no messages on the queue, continue polling
    if msg is None:
        continue

    if msg.error():
        print("AvroConsumer error: {}".format(msg.error()))
        continue

    print(msg.value())
    print(msg.key())

c.close()