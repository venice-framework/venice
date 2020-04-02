from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

import os
import requests
import time

from admin_api import CustomAdmin

BROKER = os.environ['BROKER']
SCHEMA_REGISTRY_URL = os.environ['SCHEMA_REGISTRY_URL']
# TOPIC_NAME = os.environ['TOPIC_NAME']
TOPIC_NAME = "locations"


# sleep to give the schema-registry time to connect to kafka
# Can we set this up so it waits for schema-registry and then launches. So if it crashes or needs to be restarted it can do that instantly.
for i in range(5): # dropped this because its annoying to wait 2 minutes!
  print("I am sleeping for {} seconds".format(i))
  time.sleep(1)
print("I am done sleeping")

# create a topic if it doesn't exist yet
admin = CustomAdmin(BROKER)
if not admin.topic_exists(TOPIC_NAME):
  admin.create_topics([TOPIC_NAME])

value_schema = avro.loads("""
    {
        "namespace": "septa.bus.location",
        "name": "value",
        "type": "record",
        "fields": [
            {"name": "bus_id", "type": "string", "doc": "longitude"},
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
       "type" : "string"
     }
   ]
}
""")

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

avroProducer = AvroProducer(
  {
    'bootstrap.servers': BROKER,
    'on_delivery': delivery_report,
    'schema.registry.url': SCHEMA_REGISTRY_URL
  },
  default_key_schema=key_schema,
  default_value_schema=value_schema
)

lat = 40.043152
lng = -75.18071
bus_id = 1

while True:
  for i in range(5):
    value = {
      "bus_id": str(bus_id),
      "lat": lat,
      "lng": lng
    }
    key = {
      "bus_id": str(bus_id)
    }


    avroProducer.produce(topic=TOPIC_NAME, value=value, key=key)
    print("I just produced bus:{} lat: {}, lng: {}".format(bus_id, lat, lng))
    lat += 0.000001
    lng += 0.000001
    bus_id += 1
  avroProducer.flush()
  print("I have flushed")
  time.sleep(5)


# ==============================================
#record_schema_str = avro.loads("""
#{
#   "namespace": "septa.bus.location",
#   "name": "Location",
#   "type": "record",
#   "fields" : [
#     {
#       "name" : "lat",
#       "type" : "float",
#       "doc" : "latitude"
#     },
#     {
#       "name" : "lng",
#       "type" : "float",
#       "doc" : "longitude"
#     },
#     {
#       "name" : "direction",
#       "type" : "string",
#       "doc" : "the direction the bus is traveling",
#     },
#     {
#       "name" : "route",
#       "type" : "integer"
#       "doc" : "the bus route"
#     }
#   ]
#}
#""")

#key_schema_str = """
#{
#   "namespace": "septa.bus.location",
#   "name": "key",
#   "type": "record",
#   "fields" : [
#     {
#       "name" : "trip",
#       "type" : "integer"
#     }
#   ]
#}
#"""
#
#
#value_schema = avro.loads(value_schema_str)
#value = {
#  "lat": 40.043152,
#  "lng": -75.18071,
#  "direction": "NorthBound",
#  "route": 47
#}
#
#value = {
#  "lat": 40.043152,
#  "lng": -75.18071
#}