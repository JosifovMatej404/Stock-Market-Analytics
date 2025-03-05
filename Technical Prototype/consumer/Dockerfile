FROM python:3.9

# Install Java for Spark
RUN apt-get update && apt-get install -y openjdk-11-jdk && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME environment variable
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

WORKDIR /app

# Copy consumer script
COPY kafka_consumer.py .

# Install Python dependencies
RUN pip install kafka-python pyspark

CMD ["python", "kafka_consumer.py"]
