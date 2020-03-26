import os
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

BROKER = os.environ['BROKER']
SCHEMA_REGISTRY_URL = os.environ['SCHEMA_REGISTRY_URL']

print(BROKER)
print(SCHEMA_REGISTRY_URL)

value_schema_str = """
{
   "namespace": "ui.test",
   "name": "value",
   "type": "record",
   "fields" : [
     {
       "name" : "id",
       "type" : "int"
     },
     {
       "name" : "name",
       "type" : "string"
     },
     {
       "name" : "url",
       "type" : "string"
     }
   ]
}
"""

value_schema = avro.loads(value_schema_str)
value = {"id": 1,
         "name": "user1",
         "url": "venice.com"
         }

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

avroProducer.produce(topic='clicks', value=value)
avroProducer.flush()