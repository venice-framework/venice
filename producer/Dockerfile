FROM python:3.5
# REMINDER: you will need to run apt-get update
# if you want to apt-get install anything, because 
# there isn't a package cache in the image yet
RUN pip install "confluent-kafka[avro]" requests
COPY producer.py . 
#ENTRYPOINT ["tail", "-f", "/dev/null"]
ENTRYPOINT ["python", "producer.py"]