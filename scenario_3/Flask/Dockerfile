FROM python:3.8.10
COPY . .
RUN pip install -r requirements.txt
ENV PROJECT_HOME=/code
RUN ["chmod", "777", "/start.sh"]
RUN ["chmod", "777", "/code/resources/web/mongo_seed.py"]
RUN ["chmod", "777", "/code/resources/web/create_topic.py"]
RUN ["chmod", "777", "/code/resources/web/predict_flask_kf_cs.py"]
#ENV BOOTSTRAP_SERVERS=kafka:29092
#ENV MONGODB_HOST=mongodb
#ENV MONGODB_PORT=27017
EXPOSE 5000
CMD /start.sh

