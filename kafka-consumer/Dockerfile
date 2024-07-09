FROM python:3.8-slim

# Install required packages
RUN pip install kafka-python

# Copy the consumer script
COPY kafka_consumer.py /app/kafka_consumer.py

# Set the working directory
WORKDIR /app

# Run the consumer script
CMD ["python", "kafka_consumer.py"]
