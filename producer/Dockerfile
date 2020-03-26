FROM python:3.5
# need to run apt-get update because
# there isn't a package cache in the image yet
RUN apt-get update && apt-get install netcat -y
#RUN pip install "confluent-kafka[avro]" requests
#COPY producer.py . 
#CMD ["ping", "schema-registry"]
#CMD ["ping", "-c 3", "amazon.com"]
#CMD ["ping", "-c 3", "schema-registry"]
CMD ["nc", "-vz", "schema-registry.confluent_kafka", "8081"]
#CMD ["python", "producer.py"]