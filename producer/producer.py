from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

import os
import requests
import time

from admin_api import CustomAdmin

"""
This is an example with fake data intended to demonstrate basic
functionality of the pipeline.

The context is a bus updating its location in physical space as
it moves.

The key is bus_id and the values are lat and lng.

Every event represents a location change.
The latitude and longitude are changes by a constant value
with every event.
"""

BROKER = os.environ['BROKER']
SCHEMA_REGISTRY_URL = os.environ['SCHEMA_REGISTRY_URL']
TOPIC_NAME = os.environ['TOPIC_NAME']

def delivery_report(err, msg):
    """
    Called once for each message produced to indicate delivery result.
    Triggered by poll() or flush().
    """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.
        format(msg.topic(), msg.partition()))


# Create a topic if it doesn't exist yet
admin = CustomAdmin(BROKER)
if not admin.topic_exists(TOPIC_NAME):
  admin.create_topics([TOPIC_NAME])

# Define schemas
value_schema = avro.loads("""
    {
        "namespace": "septa.bus.location",
        "name": "value",
        "type": "record",
        "fields": [
            {"name": "lat", "type": "float", "doc": "latitude"},
            {"name": "lng", "type": "float", "doc": "longitude"}
        ]
    }
""")

key_schema = avro.loads("""
{
   "namespace": "septa.bus.location",
   "name": "key",
   "type": "record",
   "fields" : [
     {
       "name" : "bus_id",
       "type" : "int"
     }
   ]
}
""")

# Initialize producer
avroProducer = AvroProducer(
  {
    'bootstrap.servers': BROKER,
    'on_delivery': delivery_report,
    'schema.registry.url': SCHEMA_REGISTRY_URL
  },
  default_key_schema=key_schema,
  default_value_schema=value_schema
)

# Initialize key and values
key = {"bus_id": 1}
lat = 40.043152
lng = -75.18071

# Produce events simulating bus movements, forever
while True:
  for i in range(5):
    value = {
      "lat": lat,
      "lng": lng 
    }
    avroProducer.produce(topic=TOPIC_NAME, value=value, key=key)
    print("I just produced bus:{} lat: {}, lng: {}".format(bus_id, lat, lng))
    lat += 0.000001
    lng += 0.000001
  avroProducer.flush()
  print("I have flushed")
  time.sleep(5)