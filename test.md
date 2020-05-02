kafka-producer-perf-test --topic test --num-records 100000 --throughput -3 --producer-props bootstrap.servers=broker-2:9092 acks=1 linger.ms=100000 buffer.memory=4294967296 request.timeout.ms=300000 delivery.timeout.ms=400000 --record-size 1000

kafka-consumer-perf-test --topic test --broker-list=broker-2:9092 --messages 100000 --threads 2
