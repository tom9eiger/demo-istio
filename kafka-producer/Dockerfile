FROM python:3.8-slim

# Install required packages
RUN pip install kafka-python requests

# Copy the producer script
COPY kafka_producer.py /app/kafka_producer.py

# Set the working directory
WORKDIR /app

# Run the producer script
CMD ["python", "kafka_producer.py"]