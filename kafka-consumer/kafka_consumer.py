import os
import logging
from kafka import KafkaConsumer
from kafka.errors import KafkaError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

broker_url = os.getenv('KAFKA_BROKER_URL', 'kafka-service.kafka.svc.cluster.local:29092')
topic = os.getenv('KAFKA_TOPIC', 'test-topic')

logger.info(f"Connecting to Kafka broker at {broker_url}")
logger.info(f"Subscribing to topic {topic}")

try:
    consumer = KafkaConsumer(topic, bootstrap_servers=[broker_url])
    logger.info("Successfully connected to Kafka broker")
except KafkaError as e:
    logger.error(f"Error connecting to Kafka broker: {e}")
    raise

for message in consumer:
    logger.info(f"Received message: {message.value.decode('utf-8')}")