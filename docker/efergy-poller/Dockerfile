FROM python:3
ENV INFLUXDB_DB="efergy" \
    INFLUXDB_URL="http://efergy-influx:8087" \
    APPDIR=/usr/src/app
WORKDIR $APPDIR
RUN apt-get update -y
RUN apt-get install tzdata cron -yqq
COPY efergy-poller.py $APPDIR/
COPY crontab /etc/cron.d/efergy-poller
COPY export_env.sh $APPDIR/
RUN chmod 0644 /etc/cron.d/efergy-poller
RUN touch /var/log/cron.log
RUN pip install --upgrade pip
RUN pip install influxdb
RUN echo "America/New_York" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

CMD ["sh", "-c", "/usr/src/app/export_env.sh && cron && tail -f /var/log/cron.log"]
