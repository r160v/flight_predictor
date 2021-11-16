from kafka import KafkaConsumer
import json, os

kafka_BSServ = os.environ["BOOTSTRAP_SERVERS"]

kafka_BS_servers=[server.strip() for server in kafka_BSServ.split(";")]
consumer = KafkaConsumer('flight_prediction_response', bootstrap_servers=kafka_BS_servers)
# consumer = KafkaConsumer('flight_prediction_response', bootstrap_servers=['localhost:29092'])
# print(consumer.topics())
for message in consumer:
  my_json = json.loads(message.value.decode('utf8').replace("'", '"'))
  print(my_json[0]["Prediction"])

