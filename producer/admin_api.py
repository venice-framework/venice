from confluent_kafka.admin import AdminClient, NewTopic, NewPartitions, ConfigResource, ConfigSource
from confluent_kafka import KafkaException
import sys
import threading
import logging

# Reference:
# https://github.com/confluentinc/confluent-kafka-python/blob/master/examples/adminapi.py

class CustomAdmin:
  def __init__(self, broker):
      self.admin = AdminClient({'bootstrap.servers': broker})

  def topic_exists(self, topic_name):
    """Return True if topic exists, False otherwise"""
    metadata = self.admin.list_topics(timeout=10)
    return topic_name in metadata.topics
  
  def create_topics(self, topic_names):
      """ Create topics """
  
      new_topics = [NewTopic(topic_name, num_partitions=3, replication_factor=1) for topic_name in topic_names]
      # Call create_topics to asynchronously create topics, a dict
      # of <topic,future> is returned.
      futures = self.admin.create_topics(new_topics)
  
      # Wait for operation to finish.
      # Timeouts are preferably controlled by passing request_timeout=15.0
      # to the create_topics() call.
      # All futures will finish at the same time.
      for topic, future in futures.items():
          try:
              future.result()  # The result itself is None
              print("Topic created: {}".format(topic))
          except Exception as e:
              print("Failed to create topic {}: {}".format(topic, e))

  def print_all_metadata(self, args=[]):
      """ list topics and cluster metadata """
      """ this is copied almost entirely from the reference file"""
  
      if len(args) == 0:
          what = "all"
      else:
          what = args[0]
  
      md = self.admin.list_topics(timeout=10)
  
      print("Cluster {} metadata (response from broker {}):".format(md.cluster_id, md.orig_broker_name))
  
      if what in ("all", "brokers"):
          print(" {} brokers:".format(len(md.brokers)))
          for b in iter(md.brokers.values()):
              if b.id == md.controller_id:
                  print("  {}  (controller)".format(b))
              else:
                  print("  {}".format(b))
  
      if what not in ("all", "topics"):
          return
  
      print(" {} topics:".format(len(md.topics)))
      for t in iter(md.topics.values()):
          if t.error is not None:
              errstr = ": {}".format(t.error)
          else:
              errstr = ""
  
          print("  \"{}\" with {} partition(s){}".format(t, len(t.partitions), errstr))
  
          for p in iter(t.partitions.values()):
              if p.error is not None:
                  errstr = ": {}".format(p.error)
              else:
                  errstr = ""
  
              print("    partition {} leader: {}, replicas: {}, isrs: {}".format(
                  p.id, p.leader, p.replicas, p.isrs, errstr))