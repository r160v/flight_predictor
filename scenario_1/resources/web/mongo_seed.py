import json
from pymongo import MongoClient
from bson import json_util

client = MongoClient('localhost', 27017)
db = client['agile_data_science']
flight_collection = db['origin_dest_distances']

# with open('origin_dest_distances.jsonl') as f:
#     file_data = json.load(f)

with open('origin_dest_distances.jsonl') as f:
    for line in f:
        document = json_util.loads(line)
        flight_collection.insert_one(document)

# if pymongo < 3.0, use insert()
# collection_currency.insert(file_data)
# if pymongo >= 3.0 use insert_one() for inserting one document
# collection_currency.insert_one(file_data)
# if pymongo >= 3.0 use insert_many() for inserting many documents
# flight_collection.insert_many(file_data)

client.close()