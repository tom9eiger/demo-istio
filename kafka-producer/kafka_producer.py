import requests
from kafka import KafkaProducer

# Get JWT token
response = requests.post('http://<jwt_issuer_ip>:3000/generate', json={'username': 'producer'})
token = response.json()['token']

producer = KafkaProducer(
    bootstrap_servers='<kafka_ingress_gateway_ip>:9092',
    security_protocol='SASL_PLAINTEXT',
    sasl_mechanism='PLAIN',
    sasl_plain_username='jwt',
    sasl_plain_password=token
)
producer.send('test-topic', b'Hello, Kafka from external producer with JWT!')
producer.flush()
print("Message sent to Kafka")
d