# version: 0.0.1
FROM ubuntu:16.04
MAINTAINER ngc7293 "feizhaoye@gmail.com"

RUN apt-get update
RUN apt-get install -y python
RUN apt-get install -y python-pip
RUN pip install flask

ADD maze /home/project/maze

WORKDIR /home/project/maze

EXPOSE 8765