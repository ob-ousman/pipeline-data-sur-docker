# Ce script lit des données de capteurs depuis Kafka, les filtre et les écrit dans MongoDB.
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, FloatType

# Initialiser la session Spark
spark = SparkSession.builder \
    .appName("IoTPipeline") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,org.mongodb.spark:mongo-spark-connector_2.12:10.2.1") \
    .getOrCreate()

# Définir le schéma des messages JSON
schema = StructType([
    StructField("sensor_id", StringType(), False),
    StructField("timestamp", StringType(), False),
    StructField("temperature", FloatType(), True),
    StructField("humidity", FloatType(), True),
    StructField("status", StringType(), True),
    StructField("location", StringType(), True)
])

# Lire le flux Kafka
df = spark .readStream.format("kafka").option("kafka.bootstrap.servers", "kafka:9092").option("subscribe", "iot-topic").load()

# Convertir la colonne value (JSON binaire) en structure
df_parsed = df.selectExpr("CAST(value AS STRING)").select(from_json(col("value"), schema).alias("data")).select("data.*")

# Appliquer le filtrage
filtered_df = df_parsed.filter((col("temperature") > 50) | (col("status") == "error"))

# Écrire le flux filtré dans MongoDB
query = filtered_df \
    .writeStream \
    .format("mongodb") \
    .option("spark.mongodb.connection.uri", "mongodb://mongodb:27017/iotdb.alerts?authSource=admin") \
    .option("checkpointLocation", "/tmp/spark-checkpoint") \
    .outputMode("append") \
    .start()

# Attendre la fin du traitement
query.awaitTermination()