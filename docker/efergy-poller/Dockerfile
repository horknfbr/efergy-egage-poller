FROM python:3

WORKDIR /usr/src/app

ENV INFLUXDB_DB="efergy" \
    INFLUXDB_URL="http://efergy-influx:8087"

COPY . .

RUN pip install influxdb python-daemon


CMD [ "python", "efergy-poller.py" ]
