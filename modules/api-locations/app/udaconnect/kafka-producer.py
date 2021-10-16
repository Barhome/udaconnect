from kafka import KafkaProducer
from flask import g

# creating a Kafka producer
TOPIC_NAME = 'items'
KAFKA_SERVER = 'localhost:9092'
producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)
#to use the producer in other parts in the app
g.kafka_producer = producer
