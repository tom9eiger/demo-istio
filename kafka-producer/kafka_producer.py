import requests
from kafka import KafkaProducer

# Get JWT token
response = requests.post('http://<jwt_issuer_ip>:3000/generate', json={'username': 'producer'})
token = response.json()['token']

producer = KafkaProducer(
    bootstrap_servers='192.168.49.241:29092',
    security_protocol='SASL_PLAINTEXT',
    sasl_mechanism='PLAIN',
    sasl_plain_username='jwt',
    sasl_plain_password=token
)
producer.send('test-topic', b'Hello, Kafka from external producer with JWT!')
producer.flush()
print("Message sent to Kafka")
d