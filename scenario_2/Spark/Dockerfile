FROM ubuntu:20.04
RUN apt-get update && \
    apt-get install -y openjdk-8-jdk && \
    apt-get install -y ant && \
    apt-get clean;
    
# Fix certificate issues
RUN apt-get update && \
    apt-get install ca-certificates-java && \
    apt-get clean && \
    update-ca-certificates -f;

# Setup JAVA_HOME -- useful for docker commandline
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
RUN export JAVA_HOME
COPY ./spark /opt/spark
COPY ./models /spark_models/models
COPY ./flight_prediction_2.12-0.1.jar /
COPY ./start.sh /
RUN chmod -R 777 /opt/spark
RUN chmod -R 777 /flight_prediction_2.12-0.1.jar
RUN chmod -R 777 /start.sh
ENV SPARK_HOME=/opt/spark
RUN export SPARK_HOME
CMD /start.sh

