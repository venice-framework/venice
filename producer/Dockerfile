FROM python:3.5
RUN apt-get install telnetd -y
RUN pip install "confluent-kafka[avro]" requests
COPY producer.py . 
#CMD ["ping", "schema-registry"]
CMD ["telnet", "schema-registry 8081"]
#CMD ["python", "producer.py"]