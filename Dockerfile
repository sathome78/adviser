FROM python:3.6.5
MAINTAINER Dmitry Gamanenko
ADD . /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt 
RUN ["chmod", "+x", "./migrate_collect_run.sh"]
ENTRYPOINT ["./migrate_collect_run.sh"]
EXPOSE 8000
