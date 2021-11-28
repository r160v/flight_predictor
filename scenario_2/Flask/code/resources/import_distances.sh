#!/bin/bash

# Import our enriched airline data as the 'airlines' collection
mongoimport --host=mongodb:27017 -d agile_data_science -c origin_dest_distances --file data/origin_dest_distances.jsonl
mongo --host=mongodb:27017 agile_data_science --eval 'db.origin_dest_distances.createIndex({Origin: 1, Dest: 1})'
