FROM python:3-slim

RUN apt-get update && apt-get install -y cron
RUN yes | apt-get install software-properties-common
RUN apt-get install dialog apt-utils -y
RUN pip install -q --no-cache-dir --upgrade pip
COPY crontab /etc/cron.d/crawler-cron
RUN chmod 0644 /etc/cron.d/crawler-cron
RUN crontab /etc/cron.d/crawler-cron

ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
CMD cron -f
