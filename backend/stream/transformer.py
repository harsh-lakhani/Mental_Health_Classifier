import pandas as pd
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
import json
from kafka import KafkaConsumer, KafkaProducer


class Receiver:
    def __init__(self, spark, topic,output_topic):
        self.topic = topic 
        self.output_topic = output_topic
        self.spark = spark
        self.consumer = KafkaConsumer(self.topic, bootstrap_servers='localhost:9092', value_deserializer=lambda m: json.loads(m.decode('utf-8')))
        self.producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        self.is_stop = False
    def start(self):
        for msg in self.consumer:
            if self.is_stop:
                return
            print("Received message:", msg.value)  # Print received message for verification
            data = [msg.value]
            df = self.spark.createDataFrame(data, schema=["id", "title"])
        
            # Convert Spark DataFrame to Pandas DataFrame
            pandas_df = df.toPandas()   
            # print("Sending DataFrame to Kafka:", pandas_df)  # Print the DataFrame to be sent to Kafka
            
            # Send the Pandas DataFrame to the 'machine_learning' Kafka topic
            self.producer.send(self.output_topic, pandas_df.to_dict(orient='records')) 
    def stop(self):
        self.is_stop = True