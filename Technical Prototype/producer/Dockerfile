FROM python:3.9

WORKDIR /app

COPY kafka_producer.py .

RUN pip install kafka-python yfinance

CMD ["python", "kafka_producer.py"]
