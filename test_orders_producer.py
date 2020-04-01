from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

import os
import requests
import time

from admin_api import CustomAdmin

BROKER = os.environ['BROKER']
SCHEMA_REGISTRY_URL = os.environ['SCHEMA_REGISTRY_URL']
TOPIC_NAME = 'orders'

# create a topic if it doesn't exist yet
admin = CustomAdmin(BROKER)
if not admin.topic_exists(TOPIC_NAME):
  admin.create_topics([TOPIC_NAME])

value_schema = avro.loads("""
{
"type":"record",
"name":"myrecord",
"fields":[
  {"name":"id","type":"int"},
  {"name":"product", "type": "string"},
  {"name":"quantity", "type": "int"},
  {"name":"price", "type": "float"}]
}
""")

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

avroProducer = AvroProducer({
    'bootstrap.servers': BROKER,
    'on_delivery': delivery_report,
    'schema.registry.url': SCHEMA_REGISTRY_URL 
    }, default_value_schema=value_schema)

value = {
"id": 999,
"product": "foo",
"quantity": 100,
"price": 50
}

avroProducer.produce(topic=TOPIC_NAME, value=value)
print("I just produced lat: {}, lng: {}".format(lat, lng))
avroProducer.flush()
print("I have flushed")