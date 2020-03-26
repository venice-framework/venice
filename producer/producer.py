import os
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

BROKER = os.environ['BROKER']
SCHEMA_REGISTRY_URL = os.environ['SCHEMA_REGISTRY_URL']

print(BROKER)
print(SCHEMA_REGISTRY_URL)

record_schema_str = avro.loads("""
{
   "namespace": "septa.bus.location",
   "name": "value",
   "type": "record",
   "fields" : [
     {
       "name" : "lat",
       "type" : "float",
       "doc" : "latitude"
     },
     {
       "name" : "lng",
       "type" : "float",
       "doc" : "longitude"
     },
     {
       "name": "direction",
       "type": "enum",
       "doc": "the direction the bus is traveling",
       "symbols": ["NorthBound", "SouthBound", "EastBound", "WestBound"]
     },
     {
       "name": "route",
       "type": "integer"
     }
   ]
}
""")

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
#key = {"trip": 44802985}
#
#def delivery_report(err, msg):
#    """ Called once for each message produced to indicate delivery result.
#        Triggered by poll() or flush(). """
#    if err is not None:
#        print('Message delivery failed: {}'.format(err))
#    else:
#        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))
#
#
#avroProducer = AvroProducer({
#    'bootstrap.servers': BROKER,
#    'on_delivery': delivery_report,
#    'schema.registry.url': SCHEMA_REGISTRY_URL 
#    }, default_value_schema=value_schema)
#
#avroProducer.produce(topic='bus.locations', value=value)
#avroProducer.flush()