FROM python:3.6.5
MAINTAINER Dmitry Gamanenko
ADD . /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt 
