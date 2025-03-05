from kafka import KafkaProducer
import yfinance as yf
import json
import time

KAFKA_BROKER = "localhost:9092"
TOPIC_NAME = "stock_prices"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


def fetch_and_send():
    stock = yf.Ticker("AAPL")
    data = stock.history(period="1d", interval="5m")

    if not data.empty:
        last = data.iloc[-1]
        stock_data = {
            "symbol": "AAPL",
            "timestamp": str(last.name),
            "open": last["Open"],
            "high": last["High"],
            "low": last["Low"],
            "close": last["Close"],
            "volume": last["Volume"]
        }
        producer.send(TOPIC_NAME, stock_data)
        print("Sent:", stock_data)


while True:
    fetch_and_send()
    time.sleep(5)  # Fetch every 5 seconds
