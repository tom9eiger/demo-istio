import os
from kafka import KafkaConsumer

broker_url = os.getenv('KAFKA_BROKER_URL', 'localhost:9092')
topic = os.getenv('KAFKA_TOPIC', 'test-topic')

consumer = KafkaConsumer(topic, bootstrap_servers=[broker_url])

for message in consumer:
    print(f"Received message: {message.value.decode('utf-8')}")
