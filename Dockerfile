FROM ubuntu:latest

RUN apt-get update -y
RUN apt-get update && apt-get -y upgrade && apt-get -y install python3 python3-pip
RUN apt-get install -y python3-pymssql
RUN apt-get install -y python3-sqlalchemy
RUN apt-get install -y python3-sqlalchemy-utils

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt --break-system-packages

ADD src /app/src

COPY aprstosql.py .

CMD ./aprstosql.py
