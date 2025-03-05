from kafka import KafkaConsumer
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import StructType, StructField, StringType, FloatType

KAFKA_BROKER = "localhost:9092"
TOPIC_NAME = "stock_prices"

# Initialize Spark Session
spark = SparkSession.builder.appName("StockProcessor").getOrCreate()

# Define Schema
schema = StructType([
    StructField("symbol", StringType(), True),
    StructField("timestamp", StringType(), True),
    StructField("open", FloatType(), True),
    StructField("high", FloatType(), True),
    StructField("low", FloatType(), True),
    StructField("close", FloatType(), True),
    StructField("volume", FloatType(), True),
])

# Read Stream from Kafka
df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER) \
    .option("subscribe", TOPIC_NAME) \
    .load() \
    .selectExpr("CAST(value AS STRING)") \
    .select(col("value").cast("string"))

df = df.selectExpr("from_json(value, '{}') AS data".format(schema.json())) \
    .select("data.*")

# Process Data
df.writeStream.format("console") \
    .outputMode("append") \
    .start() \
    .awaitTermination()
