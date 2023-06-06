
from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from kafka import KafkaProducer
import praw
import json

def send_to_kafka(rdd):
    producer = KafkaProducer(bootstrap_servers='localhost:9092')
    
    for record in rdd.collect():
        producer.send('reddit_titles', json.dumps(record).encode('utf-8'))

    producer.flush()
    producer.close()

class SparkStreamingWrapper:
    def __init__(self,subreddit):
        self.subreddit = subreddit
        # Keep track of the IDs of seen submissions
        self.seen_ids = set()
        print('Spark Streaming Wrapper initialized.')
    def start(self, batch_interval):
        print('Starting Spark Streaming...')
        # Initialize Spark and Streaming contexts
        self.sc = SparkContext.getOrCreate()
        self.ssc = StreamingContext(self.sc, batch_interval)

        # Create a DStream that reads from the REST API endpoint
        submissions = self.ssc.socketTextStream("localhost", 9999)
        submission_titles = submissions.transform(lambda rdd: self.get_submissions(rdd))

        # Process the data and send to Kafka topic
        submission_titles.foreachRDD(send_to_kafka)

        # Start the Spark Streaming context
        self.ssc.start()
        self.ssc.awaitTermination()
    

    def stop(self):
        print('Stopping Spark Streaming...')
        try:
            self.ssc.stop(stopSparkContext=True, stopGraceFully=False)
            self.sc.stop()
        except:
            pass

    def get_submissions(self,rdd):
        # Set up Reddit API
        reddit = praw.Reddit(client_id='r_mi6b5G4SkVR-uWyp37kw',
                            client_secret='c0-p81DnRU9CB9Weq70ahiTFMqeb8g',
                            user_agent='5003-test')
        subreddit = reddit.subreddit(self.subreddit)
        # 'doesanybodyelse' very good subreddit but frequency is low
        # 'askreddit' extremely frequent but may not be relevant
        new_python = subreddit.new(limit=5)

        # Filter out duplicate submissions based on their IDs
        new_submissions = [submission for submission in new_python if submission.id not in self.seen_ids]
        self.seen_ids.update(submission.id for submission in new_submissions)

        # Convert the submission titles to a list and return as a new RDD
        return rdd.context.parallelize([{"id": submission.id, "title": submission.title} for submission in new_submissions])
    
