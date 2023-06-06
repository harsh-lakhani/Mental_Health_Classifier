
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.ml.feature import Tokenizer, StopWordsRemover, CountVectorizer, IDF
from pyspark.ml.feature import StringIndexer
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import PipelineModel
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from kafka import KafkaConsumer
import pyodbc 

import json
class MLModel(object):
    def __init__(self,spark,path, topic):
        self.model = PipelineModel.load(path)
        self.spark = spark
        self.topic = topic
        self.consumer = KafkaConsumer(
            self.topic, 
            bootstrap_servers='localhost:9092', 
            value_deserializer=lambda m: json.loads(m.decode('utf-8')))
        self.dbconnect = pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};'
                      'Server=tcp:azure-bdt-sql.database.windows.net,1433;'
                      'Database=azure_bdt_5003_SQL;'
                      'Uid=kmclaw;'
                      'Pwd=Naruto95!;'
                      'Encrypt=yes;'
                      'TrustServerCertificate=no;'
                      'Connection Timeout=30'
                       )
        self.dbcursor=self.dbconnect.cursor()
        self.all_results = []
        self.is_stop = False

    def predict(self, text):
        # Create a Spark DataFrame from the input text
        df = self.spark.createDataFrame([(text,StringType())], ['text'])
        # Predict the sentiment
        result = self.model.transform(df)
        # Return the prediction
        return result.first().prediction
    
    def start(self):
        for msgs in self.consumer:
            if self.is_stop:
                return
            for msg in msgs.value:
                print("Received message ML:", msg)  # Print received message for verification
                result = self.predict(msg['title'])
                print("Prediction ML:", result)
                self.all_results.append((msg['title'],result))
                self.dbcursor.execute(f'INSERT INTO ModelResults (identifier, model_result) VALUES (\'{msg['title']}\', \'{result}\')')
                self.dbconnect.commit()
    
    def get_results(self):
        return self.all_results
    
    def stop(self):
        self.is_stop = True