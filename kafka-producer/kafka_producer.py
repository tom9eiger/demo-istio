import requests
from kafka import KafkaProducer

# Get JWT token
response = requests.post('http://192.168.49.240:3000/generate', json={'username': 'testuser'})
token = response.json()['token']

producer = KafkaProducer(
    bootstrap_servers='192.168.49.241:29092',
    security_protocol='SASL_PLAINTEXT',
    sasl_mechanism='PLAIN',
    sasl_plain_username='testuser',
    sasl_plain_password=token
)
producer.send('test-topic', b'Hello, Kafka from external producer with JWT!')
producer.flush()
print("Message sent to Kafka")
d