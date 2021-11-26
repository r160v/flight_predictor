#!/bin/bash


if [ "$SPARK_MASTER_HOST" == "" ]; then	      
  SPARK_MASTER_HOST="spark"	  
fi
if [ "$SPARK_MASTER_PORT" = "" ]; then
  SPARK_MASTER_PORT=7077
fi	

echo $SPARK_MASTER_HOST

if [ "$SPARK_MODE" = "master" ]; then
  ./opt/spark/sbin/start-master.sh &
  sleep 4
  ./opt/spark/bin/spark-submit --master $SPARK_MASTER_HOST --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1,org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 ./flight_prediction_2.12-0.1.jar 
fi

if [ "$SPARK_MODE" = "worker" ]; then  
  ./opt/spark/sbin/start-worker.sh spark://"${SPARK_MASTER_HOST}":"${SPARK_MASTER_PORT}" &
  ./opt/spark/bin/spark-submit --master $SPARK_MASTER_HOST --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1,org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 ./flight_prediction_2.12-0.1.jar 
fi


