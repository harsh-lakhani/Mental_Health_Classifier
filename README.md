# 5003 Project
1. Clone the repository
2. Create a data folder in the training directory and put the data files in it
3. go to training/ml_training.ipynb and run the cells to create the ml model

4. install the requirements.txt
```
pip install -r requirements.txt
```
5. Run Kafka
```
# install
wget https://dlcdn.apache.org/kafka/3.4.0/kafka_2.13-3.4.0.tgz
tar -xzf kafka_2.13-3.4.0.tgz
# install

# run
cd kafka_2.13-3.4.0
bin/zookeeper-server-start.sh config/zookeeper.properties
bin/kafka-server-start.sh config/server.properties
```
6. Run the port
```
nc -lk 9999
```
7. Run the flask app
```
cd backend
flask run
```
8. Run the streamlit app
```
cd frontend
streamlit run Home.py
```
# Installing spark and conda
```
wget https://repo.anaconda.com/miniconda/Miniconda3-py38_23.3.1-0-Linux-x86_64.sh
bash Miniconda3-py38_23.3.1-0-Linux-x86_64.sh

wget https://downloads.apache.org/spark/spark-3.3.2/spark-3.3.2-bin-hadoop3.tgz
tar -zxvf spark-3.3.2-bin-hadoop3.tgz
sudo apt-get update
sudo apt-get install openjdk-8-jdk

# ~/.bashrc
    export SPARK_HOME="your path to the spark directory" 
    export PATH=$SPARK_HOME/bin:$PATH 
    export PYSPARK_DRIVER_PYTHON="jupyter"
    export PYSPARK_DRIVER_PYTHON_OPTS="lab"
    
source ~/.bashrc
