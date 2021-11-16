import os
from kafka.admin import KafkaAdminClient, NewTopic
import kafka

kafka_BSServ = os.environ["BOOTSTRAP_SERVERS"]
kafka_BS_servers=[server.strip() for server in kafka_BSServ.split(";")]

topics = os.environ["TOPIC_NAME"]
topics_parts = os.environ["TOPIC_PARTITIONS"]
topics_rep_factor = os.environ["TOPIC_REPLICATION"]

consumer = kafka.KafkaConsumer(group_id='test', bootstrap_servers=kafka_BS_servers)

for topic_info in zip(topics.split(";"), topics_parts.split(";"), topics_rep_factor.split(";")):
    if topic_info[0].strip() not in consumer.topics():
        admin_client = KafkaAdminClient(
            bootstrap_servers=kafka_BS_servers,
            client_id='test'
        )

        topic_list = []
        topic_list.append(NewTopic(name=topic_info[0].strip(), num_partitions=int(topic_info[1].strip()),
                                   replication_factor=int(topic_info[2].strip())))
        admin_client.create_topics(new_topics=topic_list, validate_only=False)

