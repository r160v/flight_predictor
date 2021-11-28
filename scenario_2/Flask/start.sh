#!/bin/bash

python3 /code/resources/web/mongo_seed.py
python3 /code/resources/web/create_topic.py
python3 /code/resources/web/predict_flask.py
