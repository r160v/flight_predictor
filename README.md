# Flight_Predictor
## Scenario 1: Run components Zookeeper, Kafka, MongoDB, Spark Streaming and Flask independently

# Installation
It's necessary to install the following components:

 - [Intellij](https://www.jetbrains.com/help/idea/installation-guide.html) (jdk_1.8)
 - [Pyhton3](https://realpython.com/installing-python/) (Suggested version 3.7) 
 - [PIP](https://pip.pypa.io/en/stable/installing/)
 - [SBT](https://www.scala-sbt.org/release/docs/Setup.html) 
 - [MongoDB](https://docs.mongodb.com/manual/installation/)
 - [Spark](https://spark.apache.org/docs/latest/) (Mandatory version 3.1.2)
 - [Scala](https://www.scala-lang.org)(Suggested version 2.12)
 - [Zookeeper](https://zookeeper.apache.org/releases.html)
 - [Kafka](https://kafka.apache.org/quickstart) (Mandatory version kafka_2.12-3.0.0)

### Install python libraries
 
 ```
  pip install -r requirements.txt
 ```
 ### Start Zookeeper
 
 Open a console and go to the downloaded Kafka directory and run:
 
 ```
   bin/zookeeper-server-start.sh config/zookeeper.properties
  ```
  ### Start Kafka
  
  Open a console and go to the downloaded Kafka directory and run:
  
  ```
    bin/kafka-server-start.sh config/server.properties
   ```
   open a new console in teh same directory and create a new topic :
  ```
      bin/kafka-topics.sh \
        --create \
        --bootstrap-server localhost:9092 \
        --replication-factor 1 \
        --partitions 1 \
        --topic flight_delay_classification_request
   ```
   You should see the following message:
  ```
    Created topic "flight_delay_classification_request".
  ```
  You can see the topic we created with the list topics command:
  ```
      bin/kafka-topics.sh --bootstrap-server localhost:9092 --list
  ```
  Output:
  ```
    flight_delay_classification_request
  ```
  (Optional) You can oen a new console with a consumer in order to see the messeges sent to that topic
  ```
  bin/kafka-console-consumer.sh \
      --bootstrap-server localhost:9092 \
      --topic flight_delay_classification_request \
      --from-beginning
  ```
  ## Import the distance records to MongoDB
  Check if you have Mongo up and running:
  ```
  service mongod status
  ```
  Output:
  ```
  mongod.service - MongoDB Database Server
     Loaded: loaded (/lib/systemd/system/mongod.service; disabled; vendor preset: 
     Active: active (running) since Tue 2019-10-01 14:58:53 CEST; 2h 11min ago
       Docs: https://docs.mongodb.org/manual
   Main PID: 7816 (mongod)
     CGroup: /system.slice/mongod.service
             └─7816 /usr/bin/mongod --config /etc/mongod.conf
  
  oct 01 14:58:53 amunoz systemd[1]: Started MongoDB Database Server.
  ```
  Run the import_distances.sh script. **If MongoDB version is 5 or higher it's necessary to change "ensureIndex" to "createIndex" in the script.**
  ```
  ./resources/import_distances.sh
  ```
  Output:
  ```
  2019-10-01T17:06:46.957+0200	connected to: mongodb://localhost/
  2019-10-01T17:06:47.035+0200	4696 document(s) imported successfully. 0 document(s) failed to import.
  MongoDB shell version v4.2.0
  connecting to: mongodb://127.0.0.1:27017/agile_data_science?compressors=disabled&gssapiServiceName=mongodb
  Implicit session: session { "id" : UUID("9bda4bb6-5727-4e91-8855-71db2b818232") }
  MongoDB server version: 4.2.0
  {
  	"createdCollectionAutomatically" : false,
  	"numIndexesBefore" : 1,
  	"numIndexesAfter" : 2,
  	"ok" : 1
  }

  ```
  ## Train and save the model with PySpark mllib
  In a console go to the base directory of the cloned repo, then go to the `practica_big_data_2019` directory
  ```
    cd practica_big_data_2019
  ```
  Set the `JAVA_HOME` env variable with teh path of java installation directory, for example:
  ```
    export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64/bin
  ```
  Set the `SPARK_HOME` env variable with teh path of your Spark installation folder, for example:
  ```
    export SPARK_HOME=/opt/spark
  ```
  Now, execute the script `train_spark_mllib_model.py`
  ```
      python3 resources/train_spark_mllib_model.py .
  ```
  As result, some files will be saved in the `models` folder 
  
  ```
  ls ../models
  
  ```   
  ## Run Flight Predictor
  First, you need to change the base_paht val in the MakePrediction scala class,
  change that val for the path where you clone repo is placed:
  ```
    val base_path= "/home/user/Desktop/practica_big_data_2019"
    
  ``` 
  Then run the code using Intellij or spark-submit with their respective arguments. 
  
Please, note that in order to use spark-submit you first need to compile the code and build a JAR file using sbt. To compile and package the code open a terminal in the "flight_prediction" folder and run:
 ```
  sbt compile package
     
  ``` 
The .jar file will be generated in "flight_prediction/target/scala-2.12/" folder.
Also, when running the spark-submit command, you have to add at least these two packages with the --packages option:
  ```
  spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1,org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 ./<generated_package>.jar
     
  ``` 
   Be carefull with the packages version because if you are using another version of spark, kafka or mongo you have to choose the correspondent version to your installation. This packages work with Spark 2.4.0, kafka_2.12-2.3.0 and mongo superior to 2.6.
  
  ## Start the prediction request Web Application
  
  Set the `PROJECT_HOME` env variable with teh path of you cloned repository, for example:
   ```
  export PROJECT_HOME=/home/user/Desktop/practica_big_data_2019
   ```
  Go to the `web` directory under `resources` and execute the flask web application file `predict_flask.py`:
  ```
  cd practica_big_data_2019/resources/web
  python3 predict_flask.py
  
  ```
  Now, visit http://localhost:5000/flights/delays/predict_kafka and, for fun, open the JavaScript console. Enter a nonzero departure delay, an ISO-formatted date (I used 2016-12-25, which was in the future at the time I was writing this), a valid carrier code (use AA or DL if you don’t know one), an origin and destination (my favorite is ATL → SFO), and a valid flight number (e.g., 1519), and hit Submit. Watch the debug output in the JavaScript console as the client polls for data from the response endpoint at /flights/delays/predict/classify_realtime/response/.
  
  Quickly switch windows to your Spark console. Within 10 seconds, the length we’ve configured of a minibatch, you should see something like the following:
  
  ## Check the predictions records inserted in MongoDB
  ```
   $ mongo
   > use agile_data_science;
   >db.flight_delay_classification_response.find();
  
  ```
  You must have a similar output as:
  
  ```
  { "_id" : ObjectId("5d8dcb105e8b5622696d6f2e"), "Origin" : "ATL", "DayOfWeek" : 6, "DayOfYear" : 360, "DayOfMonth" : 25, "Dest" : "SFO", "DepDelay" : 290, "Timestamp" : ISODate("2019-09-27T08:40:48.175Z"), "FlightDate" : ISODate("2016-12-24T23:00:00Z"), "Carrier" : "AA", "UUID" : "8e90da7e-63f5-45f9-8f3d-7d948120e5a2", "Distance" : 2139, "Route" : "ATL-SFO", "Prediction" : 3 }
  { "_id" : ObjectId("5d8dcba85e8b562d1d0f9cb8"), "Origin" : "ATL", "DayOfWeek" : 6, "DayOfYear" : 360, "DayOfMonth" : 25, "Dest" : "SFO", "DepDelay" : 291, "Timestamp" : ISODate("2019-09-27T08:43:20.222Z"), "FlightDate" : ISODate("2016-12-24T23:00:00Z"), "Carrier" : "AA", "UUID" : "d3e44ea5-d42c-4874-b5f7-e8a62b006176", "Distance" : 2139, "Route" : "ATL-SFO", "Prediction" : 3 }
  { "_id" : ObjectId("5d8dcbe05e8b562d1d0f9cba"), "Origin" : "ATL", "DayOfWeek" : 6, "DayOfYear" : 360, "DayOfMonth" : 25, "Dest" : "SFO", "DepDelay" : 5, "Timestamp" : ISODate("2019-09-27T08:44:16.432Z"), "FlightDate" : ISODate("2016-12-24T23:00:00Z"), "Carrier" : "AA", "UUID" : "a153dfb1-172d-4232-819c-8f3687af8600", "Distance" : 2139, "Route" : "ATL-SFO", "Prediction" : 1 }


```
## Scenario 2: Flight Predictor improvements
In "scenario_2" the folders "Spark" and "Flask" are included. The original code of both components has been modified to insert some improvements. 
- Spark
As for Spark, the MakePrediction.scala file now uses environment variables to define the Kafka bootstrap servers and the MongoDB server address and port number. Besides, the environment variable `SEND_PREDICTION_TO`, located in "Build", has been added to allow Spark to send the prediction to a Kafka topic instead of to MongoDB. This removes the need of the web app to be constantly polling MongoDB until it gets a prediction. Now, the web app acts as a consumer of the Kafka topic `flight_prediction_response`, when a prediction is written to the topic, it shows it on screen. In "Spark" there is also a Dockerfile and the necessary files to build an image.
The environment variables `MONGODB_HOST`, `MONGODB_PORT`, `BOOTSTRAP_SERVERS` (if more than one separate them with commas) and `SEND_PREDICTION_TO` need to be set when running the container. If `SEND_PREDICTION_TO` is set to mongo, the predictions will be sent to MongoDB, otherwise they will be written to the topic.
- Flask (Web App)

There is a flight_predictor.yml file in "scenario2". To start Flight_Predictor use the following command:
```
docker-compose -f flight_predictor.yml up
```
Visit [http://localhost:9999/flights/delays/predict_kafka](http://localhost:9999/flights/delays/predict_kafka) to use the application.
## Scenario 3: Start Flight Predictor with docker compose. Spark Streaming predictions are written to a Kafka topic and the Flask app consume the predictions from that topic
In this case, the MakePrediction.scala file has been modified to send the predictions to a Kafka topic ("flight_prediction_response") instead of sending it to MongoDB. A Kafka consumer in Flask subscribes to that topic and the page shows the prediction after it is consumed from the topic.
The "scenario 3" folder includes a Spark and Flask folders to build the images, as well as a "flight_predictor_kf_pred_resp.yml" file to start the scenario.

```
docker-compose -f flight_predictor_kf_pred_resp.yml up
```
**When running the Flask container, it is mandatory that the environment variable `TOPIC_NAME` includes at least flight_delay_classification_request;flight_prediction_response topics.** More topics can be added (separated with a semicolon), the Flask app will create them (if don't exist) on startup. **There must be a one-to-one correspondence between each topic in `TOPIC_NAME` and each value in `TOPIC_PARTITIONS` and `TOPIC_REPLICATION`.**
```
- TOPIC_NAME=flight_delay_classification_request;flight_prediction_response
- TOPIC_PARTITIONS=1;2
- TOPIC_REPLICATION=3;4
```
To see the predictions being written to the topic flight_prediction_response, another Kafka consumer can be used. After accessing the Kafka container run the following command:
```
/bin/kafka-console-consumer \
    --bootstrap-server localhost:9092 \
    --topic flight_prediction_response \
    --from-beginning
```
Visit [http://localhost:9999/flights/delays/predict_kafka](http://localhost:9999/flights/delays/predict_kafka) to use the application.
## Scenario 4: Deploy Flight Predictor using Kubernetes and Minikube
- Install Minikube using a Docker container or virtual machine using [https://minikube.sigs.k8s.io/docs/start/](https://minikube.sigs.k8s.io/docs/start/). A minimum of 5 GB of RAM is recommended for the VM. Once installed start the container or VM.
- Open a terminal and start minikube to be able to use kubectl:
```
minikube start --vm-driver=virtualbox
```
In this case the virtualization hypervisor used is Virtualbox. If another one is used, the vm-driver flag has to be set accordingly.
- Deploy Kafka and Zookeeper
To deploy Kafka and Zookeeper, a [Bitnami Helm chart](https://artifacthub.io/packages/helm/bitnami/kafka) is used. It is important to notice that it provides the DNS name `my-release-kafka-0.my-release-kafka-headless.default.svc.cluster.local` with port `9092` to connect to the Kafka cluster from within the Kubernetes cluster. 
To add the Kafka repository use the following command:
```
helm repo add bitnami https://charts.bitnami.com/bitnami
```
To install the chart:
```
helm install my-release bitnami/kafka
```
- Deploy MondoDB
To deploy Kafka and Zookeeper, a [Bitnami Helm chart](https://artifacthub.io/packages/helm/bitnami/mongodb) is used. It is important to notice that it provides the DNS name `mongodb-dev.default.svc.cluster.local` with port `27017` to connect to the Kafka cluster from within the Kubernetes cluster. 
To add the MongoDB repository use the following command:
```
helm repo add bitnami https://charts.bitnami.com/bitnami (if you haven't previously done)
```
To install the chart:
```
helm install mongodb-dev bitnami/mongodb --set auth.enabled=false
```
- Deploy Spark
The MakePrediction.scala file has been modified to take into account the DNS names of MongoDB and Kafka in the Kubernetes cluster. There is a "Spark" folder in "scenario_4", where a new flight_prediction_2.12-0.1.jar as been compiled and packaged. After doing this, it's necessary to create a new image using the provided Dockerfile. The files spark-deployment.yaml and spark-service.yaml are provided in "scenario_4" to create the components necessary for Spark.
To deploy Spark:
```
kubectl apply -f spark-deployment.yaml
```
To deploy the Spark service:
```
kubectl apply -f spark-service.yaml
```
- Deploy Flask
To deploy Flask:
```
kubectl apply -f flask-deployment.yaml
```
To deploy the Flask service:
```
kubectl apply -f flask-service.yaml
```
The Flask service is external, it provides access to the Flask app through the nodePort 30005.
- Make Minikube assign an external IP to the Flask service
List running services and take the Flask service:
```
kubectl get services
```
Use the following command to make Minikube assign an external IP to the Flask service:
```
minikube service <flask_service>
```
Visit [http://localhost:30005/flights/delays/predict_kafka](http://localhost:30005/flights/delays/predict_kafka) to use the application.
## Train the prediction model using Apache Airflow
Airflow is a platform to programmatically author, schedule and monitor workflows. It uses Directed Acyclic Graphs (DAGs) to create data pipelines. To define a DAG a DAG definition file is used.
A DAG definition file is composed of three main parts:
- Importing modules
- Default arguments
- DAG instantiation
- Tasks definition
- Setting up dependencies
# Train the prediction model using Airflow
- Download "scenario_1" folder
- Install the requirements in the root of scenario_1 and the one in "resources/airflow":
```
cd scenario_1
pip install -r requirements.txt

cd scenario_1/resources/airflow
pip install -r requirements.txt -c constraints.txt

```
- Set the `PROJECT_HOME` env variable with the path of you cloned repository, for example:
```
export PROJECT_HOME=/home/user/Desktop/scenario_1
```
- Initialize the database tables
```
airflow db init
```
- Configure airflow environment

```shell
export AIRFLOW_HOME=~/airflow
mkdir $AIRFLOW_HOME/dags
mkdir $AIRFLOW_HOME/logs
mkdir $AIRFLOW_HOME/plugins

airflow users create \
    --username admin \
    --firstname Jack \
    --lastname  Sparrow\
    --role Admin \
    --email example@mail.org
```
- Make DAG visible to Airflow  *-*-*-*-*--*
In "resources/airflow/" there is setup.py file that defines the DAG and prediction task. The default location for the DAGs is ~/airflow/dags, but more generally it is $AIRFLOW_HOME/dags. Copy setup.py to $AIRFLOW_HOME/dags (or make a symlink).
- Make sure that the pipeline is parsed successfully
```
python $AIRFLOW_HOME/dags/setup.py
```
- Check that Airflow can see the DAG
```
airflow dags list
```
- List tasks within agile_data_science_batch_prediction_model_training dag
```
airflow tasks list agile_data_science_batch_prediction_model_training
```
In this case there's only one task: pyspark_train_classifier_model.
- Test the task using the CLI
```
airflow tasks test agile_data_science_batch_prediction_model_training pyspark_train_classifier_model 2016-12-12 /*/*/*/*/*/*/*/*/*/*/*/*/*
```
The trained model files should be generated in the "models" folder.
- Start airflow scheduler and webserver
```shell
airflow webserver --port 8080
airflow scheduler
```
Vistit http://localhost:8080/home for the web version of Apache Airflow.

