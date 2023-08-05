FROM python:3.10-bullseye

RUN apt-get -y update
RUN apt-get -y install libcmph-dev
RUN apt-get -y install librdkafka-dev

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ENV PYTHONPATH=/usr/src/app/

COPY requirements*.txt /usr/src/app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt -r requirements-swh.txt
