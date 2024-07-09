import os
import requests
from kafka import KafkaProducer

# Obtain JWT token
response = requests.post('http://jwt-issuer.jwt-issuer.svc.cluster.local:3000/token')
token = response.json()['token']

# Configure Kafka producer
producer = KafkaProducer(
    bootstrap_servers=os.getenv('KAFKA_BROKER_URL', 'kafka-service.kafka.svc.cluster.local:29092'),
    # security_protocol="SASL_PLAINTEXT",
    # sasl_mechanism="OAUTHBEARER",
    # sasl_plain_username="unused",
    # sasl_plain_password=token
)

# Send a test message
producer.send('test-topic', b'Hello, Kafka!')
producer.flush()