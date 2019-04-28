FROM python:3
ENV INFLUXDB_DB="efergy" \
    INFLUXDB_URL="http://efergy-influx:8087" \
    APPDIR=/usr/src/app
WORKDIR $APPDIR
RUN apt-get update -y
RUN apt-get install cron -yqq
COPY efergy-poller.py $APPDIR/
COPY project_env.sh $APPDIR/
COPY crontab /etc/cron.d/efergy-poller
RUN chmod 0644 /etc/cron.d/efergy-poller
RUN touch /var/log/cron.log

RUN pip install influxdb

CMD cron && tail -f /var/log/cron.log
